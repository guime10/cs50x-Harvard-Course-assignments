-- Keep a log of any SQL queries you execute as you solve the mystery.

SELECT description FROM crime_scene_reports
WHERE month = 7
AND day = 28
AND street = "Humphrey Street";

Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery. Interviews were conducted today with three witnesses who were present at the time –
each of their interview transcripts mentions the bakery.
Littering took place at 16:36. No known witnesses.

SELECT name, transcript FROM interviews
WHERE month = 7
AND day = 28

| Ruth Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

| Eugene I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery,
I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

| Raymond As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
The thief then asked the person on the other end of the phone to purchase the flight ticket.                                                                    |
| Emma    | I'm the bakery owner, and someone came in, suspiciously whispering into a phone for about half an hour. They never bought anything.

SELECT * FROM bakery_security_logs
WHERE month = 7
AND day = 28
AND hour = 10
AND minute >= 15
AND minute <= 25

+-----+------+-------+-----+------+--------+----------+---------------+
| id  | year | month | day | hour | minute | activity | license_plate |
+-----+------+-------+-----+------+--------+----------+---------------+
| 260 | 2021 | 7     | 28  | 10   | 16     | exit     | 5P2BI95       |
| 261 | 2021 | 7     | 28  | 10   | 18     | exit     | 94KL13X       |
| 262 | 2021 | 7     | 28  | 10   | 18     | exit     | 6P58WS2       |
| 263 | 2021 | 7     | 28  | 10   | 19     | exit     | 4328GD8       |
| 264 | 2021 | 7     | 28  | 10   | 20     | exit     | G412CB7       |
| 265 | 2021 | 7     | 28  | 10   | 21     | exit     | L93JTIZ       |
| 266 | 2021 | 7     | 28  | 10   | 23     | exit     | 322W7JE       |
| 267 | 2021 | 7     | 28  | 10   | 23     | exit     | 0NTHK55       |
+-----+------+-------+-----+------+--------+----------+---------------+

SELECT id, account_number, transaction_type, amount FROM atm_transactions
WHERE month = 7
AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";

+----------------+------------------+--------+
| account_number | transaction_type | amount |
+----------------+------------------+--------+
| 28500762       | withdraw         | 48     |
| 28296815       | withdraw         | 20     |
| 76054385       | withdraw         | 60     |
| 49610011       | withdraw         | 50     |
| 16153065       | withdraw         | 80     |
| 25506511       | withdraw         | 20     |
| 81061156       | withdraw         | 30     |
| 26013199       | withdraw         | 35     |
+----------------+------------------+--------+

SELECT * FROM people
JOIN atm_transactions on atm_transactions.account_number = bank_accounts.account_number
JOIN bank_accounts on people.id = bank_accounts.person_id
WHERE bank_accounts.person_id IN (
SELECT person_id FROM bank_accounts
WHERE bank_accounts.account_number IN (
SELECT account_number FROM atm_transactions
WHERE month = 7
AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw"))
ORDER BY people.name;

+---------+-----------+
|  name   | person_id |
+---------+-----------+
| Benista | 438727    |
| Benista | 438727    |
| Brooke  | 458378    |
| Bruce   | 686048    |
| Bruce   | 686048    |
| Diana   | 514354    |
| Diana   | 514354    |
| Iman    | 396669    |
| Iman    | 396669    |
| Kenny   | 395717    |
| Kenny   | 395717    |
| Luca    | 467400    |
| Luca    | 467400    |
| Taylor  | 449774    |
+---------+-----------+

possibilities THIEF = Benista, Brooke, Bruce, Diana, Iman, Kenny, Luca, Taylor

SELECT id, caller, receiver FROM phone_calls
WHERE month = 7
AND day = 28
AND duration < 60

+-----+----------------+----------------+
| id  |     caller     |    receiver    |
+-----+----------------+----------------+
| 221 | (130) 555-0289 | (996) 555-8899 |
| 224 | (499) 555-9472 | (892) 555-8872 |
| 233 | (367) 555-5533 | (375) 555-8161 | bruce
| 251 | (499) 555-9472 | (717) 555-1342 |
| 254 | (286) 555-6063 | (676) 555-6554 | taylor
| 255 | (770) 555-1861 | (725) 555-3243 |
| 261 | (031) 555-6622 | (910) 555-3251 |
| 279 | (826) 555-1652 | (066) 555-9701 |
| 281 | (338) 555-6650 | (704) 555-2131 |
+-----+----------------+----------------+
Thief - partner
Bruce - Robin
Kathryn - Luca
Taylor - James
Diana - Philip
Keeny - Doris
Benista - Anna

SELECT name, phone_number FROM people
WHERE phone_number IN (SELECT
caller FROM phone_calls
WHERE month = 7
AND day = 28
AND duration < 60)
ORDER BY name

+---------+----------------+
| Benista | (338) 555-6650 |
| Bruce   | (367) 555-5533 |
| Carina  | (031) 555-6622 |
| Diana   | (770) 555-1861 |
| Kelsey  | (499) 555-9472 |
| Kenny   | (826) 555-1652 |
| Sofia   | (130) 555-0289 |
| Taylor  | (286) 555-6063 |
+---------+----------------+

SELECT name, phone_number FROM people
WHERE phone_number IN (SELECT
receiver FROM phone_calls
WHERE month = 7
AND day = 28
AND duration < 60)
ORDER BY name


+------------+----------------+
|    name    |  phone_number  |
+------------+----------------+
| Anna       | (704) 555-2131 |
| Doris      | (066) 555-9701 |
| Jack       | (996) 555-8899 |
| Jacqueline | (910) 555-3251 |
| James      | (676) 555-6554 |
| Larry      | (892) 555-8872 |
| Melissa    | (717) 555-1342 |
| Philip     | (725) 555-3243 |
| Robin      | (375) 555-8161 |
+------------+----------------+

SELECT name, hour FROM people
WHERE license_plate IN (
SELECT license_plate FROM bakery_security_logs
WHERE month = 7
AND day = 28
AND hour <= 11)
ORDER BY name;

+---------+
|  name   |
+---------+
| Barry   |
| Brandon |
| Bruce   |
| Denise  |
| Diana   |
| Iman    |
| Jeremy  |
| Kelsey  |
| Luca    |
| Sofia   |
| Sophia  |
| Taylor  |
| Thomas  |
| Vanessa |
+---------+

Thief - partner
Bruce - Robin
Kathryn - Luca
Taylor - James
Diana - Philip

possibilities THIEF = Bruce, Diana, Taylor
*Possibilities ACCOMPLICE = Benista, Carina, Kathryn, Kelsey, Kenny (counting as they werent at the bakery)

SELECT id,abbreviation, full_name from airports
WHERE city = "Fiftyville";

+--------------+-----------------------------+
| abbreviation |          full_name          |
+--------------+-----------------------------+
| CSF          | Fiftyville Regional Airport |
+--------------+-----------------------------+

SELECT * from flights
WHERE origin_airport_id = 8
AND month = 7
AND day = 29
ORDER BY hour;

+----+-------------------+------------------------+------+-------+-----+------+--------+
| id | origin_airport_id | destination_airport_id | year | month | day | hour | minute |
+----+-------------------+------------------------+------+-------+-----+------+--------+
| 36 | 8                 | 4                      | 2021 | 7     | 29  | 8    | 20     |
| 43 | 8                 | 1                      | 2021 | 7     | 29  | 9    | 30     |
| 23 | 8                 | 11                     | 2021 | 7     | 29  | 12   | 15     |
| 53 | 8                 | 9                      | 2021 | 7     | 29  | 15   | 20     |
| 18 | 8                 | 6                      | 2021 | 7     | 29  | 16   | 0      |
+----+-------------------+------------------------+------+-------+-----+------+--------+

SELECT * from airports
WHERE id IN (SELECT destination_airport_id from flights
WHERE origin_airport_id = 8
AND month = 7
AND day = 29)
ORDER BY full_name;

+----+--------------+-------------------------------------+---------------+
| id | abbreviation |              full_name              |     city      |
+----+--------------+-------------------------------------+---------------+
| 4  | LGA          | LaGuardia Airport                   | New York City |
| 6  | BOS          | Logan International Airport         | Boston        |
| 1  | ORD          | O'Hare International Airport        | Chicago       |
| 11 | SFO          | San Francisco International Airport | San Francisco |
| 9  | HND          | Tokyo International Airport         | Tokyo         |
+----+--------------+-------------------------------------+---------------+

SELECT * FROM passengers
WHERE flight_id = 36;

+-----------+-----------------+------+
| flight_id | passport_number | seat |
+-----------+-----------------+------+
| 36        | 7214083635      | 2A   |
| 36        | 1695452385      | 3B   |
| 36        | 5773159633      | 4A   |
| 36        | 1540955065      | 5C   |
| 36        | 8294398571      | 6C   |
| 36        | 1988161715      | 6D   |
| 36        | 9878712108      | 7A   |
| 36        | 8496433585      | 7B   |
+-----------+-----------------+------+

SELECT * from people
WHERE passport_number IN (
SELECT passport_number FROM passengers
WHERE flight_id = 36)
ORDER BY name;

+--------+--------+----------------+-----------------+---------------+
|   id   |  name  |  phone_number  | passport_number | license_plate |
+--------+--------+----------------+-----------------+---------------+
| 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
| 953679 | Doris  | (066) 555-9701 | 7214083635      | M51FA04       |
| 651714 | Edward | (328) 555-1152 | 1540955065      | 130LD9Z       |
| 560886 | Kelsey | (499) 555-9472 | 8294398571      | 0NTHK55       |
| 395717 | Kenny  | (826) 555-1652 | 9878712108      | 30G67EN       |
| 467400 | Luca   | (389) 555-5198 | 8496433585      | 4328GD8       |
| 398010 | Sofia  | (130) 555-0289 | 1695452385      | G412CB7       |
| 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
+--------+--------+----------------+-----------------+---------------+

SELECT * from people
WHERE passport_number IN (
SELECT passport_number FROM passengers
WHERE flight_id = 36)
AND license_plate IN (
SELECT license_plate FROM bakery_security_logs
WHERE month = 7
AND day = 28
AND hour = 10
AND minute >= 15
AND minute <= 25)
AND phone_number in (SELECT
caller FROM phone_calls
WHERE month = 7
AND day = 28
AND duration <= 60)
ORDER BY name;

suspects with license plate, caller-receiver and passport:
+--------+--------+----------------+-----------------+---------------+
|   id   |  name  |  phone_number  | passport_number | license_plate |
+--------+--------+----------------+-----------------+---------------+
| 686048 | Bruce  | (367) 555-5533 | 5773159633      | 94KL13X       |
| 560886 | Kelsey | (499) 555-9472 | 8294398571      | 0NTHK55       |
| 398010 | Sofia  | (130) 555-0289 | 1695452385      | G412CB7       |
| 449774 | Taylor | (286) 555-6063 | 1988161715      | 1106N58       |
+--------+--------+----------------+-----------------+---------------+

Thief - partner
Bruce - Robin
Taylor - James

SELECT * from people
WHERE passport_number IN (
SELECT passport_number FROM passengers
WHERE flight_id = 36)
AND phone_number IN (SELECT phone_number FROM people
WHERE phone_number IN (SELECT
caller FROM phone_calls
WHERE month = 7
AND day = 28
AND duration < 60))
AND license_plate IN (
SELECT license_plate FROM bakery_security_logs
WHERE month = 7
AND day = 28
AND hour = 10
AND minute >= 15
AND minute <= 25)
AND id IN (SELECT bank_accounts.person_id FROM people
JOIN atm_transactions on atm_transactions.account_number = bank_accounts.account_number
JOIN bank_accounts on people.id = bank_accounts.person_id
WHERE bank_accounts.person_id IN (
SELECT person_id FROM bank_accounts
WHERE bank_accounts.account_number IN (
SELECT account_number FROM atm_transactions
WHERE month = 7
AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw")))
ORDER BY name;


+--------+-------+----------------+-----------------+---------------+
|   id   | name  |  phone_number  | passport_number | license_plate |
+--------+-------+----------------+-----------------+---------------+
| 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
+--------+-------+----------------+-----------------+---------------+

Thief - partner
Bruce(c) - Robin(r)