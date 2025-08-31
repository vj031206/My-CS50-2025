-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports WHERE street = 'Humphrey Street' AND day = 28 AND month = 7; --took place at 10:15am, 3 witnesses, each mentions bakery
SELECT * FROM interviews WHERE day = 28 AND month = 7;

-- | 161 | Ruth    | 2024 | 7     | 28  | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.
SELECT * FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND activity = 'exit' AND minute <= 25; -- 8 people left within 10 min of theft, suspect is one of these
SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND activity = 'exit' AND minute <= 25; -- those 8 license plates on 28 July
SELECT * FROM people WHERE license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit'); -- those people's details having those 8 license plates
-- +--------+---------+----------------+-----------------+---------------+
-- |   id   |  name   |  phone_number  | passport_number | license_plate |
-- +--------+---------+----------------+-----------------+---------------+
-- | 221103 | Vanessa | (725) 555-4692 | 2963008352      | 5P2BI95       |
-- | 243696 | Barry   | (301) 555-4174 | 7526138472      | 6P58WS2       |
-- | 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- | 398010 | Sofia   | (130) 555-0289 | 1695452385      | G412CB7       |
-- | 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | 560886 | Kelsey  | (499) 555-9472 | 8294398571      | 0NTHK55       |
-- | 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
-- +--------+---------+----------------+-----------------+---------------+

-- | 162 | Eugene  | 2024 | 7     | 28  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.
SELECT * FROM atm_transactions WHERE day = 28 AND month = 7 AND atm_location = 'Leggett Street' AND transaction_type = 'withdraw'; -- 8 people withdrew money from leggett street atm on that day
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND atm_location = 'Leggett Street')); -- those 8 people details
-- +--------+---------+----------------+-----------------+---------------+
-- |   id   |  name   |  phone_number  | passport_number | license_plate |
-- +--------+---------+----------------+-----------------+---------------+
-- | 395717 | Kenny   | (826) 555-1652 | 9878712108      | 30G67EN       |
-- | 396669 | Iman    | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- | 438727 | Benista | (338) 555-6650 | 9586786673      | 8X428L0       |
-- | 449774 | Taylor  | (286) 555-6063 | 1988161715      | 1106N58       |
-- | 458378 | Brooke  | (122) 555-4581 | 4408372428      | QX4YZN3       |
-- | 467400 | Luca    | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 514354 | Diana   | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | 686048 | Bruce   | (367) 555-5533 | 5773159633      | 94KL13X       |
-- | 948985 | Kaelyn  | (098) 555-1164 | 8304650265      | I449449       |
-- +--------+---------+----------------+-----------------+---------------+
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND atm_location = 'Leggett Street')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit');
-- +--------+-------+----------------+-----------------+---------------+ 4 people who both made a withdrawal from leggett street and exited bakery within 10 mins of theft
-- |   id   | name  |  phone_number  | passport_number | license_plate |
-- +--------+-------+----------------+-----------------+---------------+
-- | 396669 | Iman  | (829) 555-5269 | 7049073643      | L93JTIZ       |
-- | 467400 | Luca  | (389) 555-5198 | 8496433585      | 4328GD8       |
-- | 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
-- +--------+-------+----------------+-----------------+---------------+
                                                                                                 |
-- | 163 | Raymond | 2024 | 7     | 28  | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
SELECT * FROM phone_calls WHERE day = 28 AND month = 7 AND duration <= 60;
SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND atm_location = 'Leggett Street')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit') AND phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND duration <= 60);
-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate | 2 people who made the withdrawal, exited bakery and called for less than a minute
-- +--------+-------+----------------+-----------------+---------------+ ie 2 narrowed suspects
-- | 514354 | Diana | (770) 555-1861 | 3592750733      | 322W7JE       |
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
-- +--------+-------+----------------+-----------------+---------------+
SELECT receiver FROM phone_calls WHERE day = 28 AND month = 7 AND caller IN (SELECT phone_number FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND atm_location = 'Leggett Street')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit') AND phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND duration <= 60));
-- +----------------+
-- |    receiver    | 4 receivers of the calls made by those 2 and their details
-- +----------------+
-- | (375) 555-8161 |
-- | (344) 555-9601 |
-- | (022) 555-4052 |
-- | (725) 555-3243 |
-- | (704) 555-5790 |
-- +----------------+
SELECT * FROM people WHERE phone_number IN (SELECT receiver FROM phone_calls WHERE day = 28 AND month = 7 AND caller IN (SELECT phone_number FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND atm_location = 'Leggett Street')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit') AND phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND duration <= 60)));
-- +--------+---------+----------------+-----------------+---------------+
-- |   id   |  name   |  phone_number  | passport_number | license_plate | details of possible accomplices
-- +--------+---------+----------------+-----------------+---------------+
-- | 315221 | Gregory | (022) 555-4052 | 3355598951      | V4C670D       |
-- | 652398 | Carl    | (704) 555-5790 | 7771405611      | 81MZ921       |
-- | 847116 | Philip  | (725) 555-3243 | 3391710505      | GW362R6       |
-- | 864400 | Robin   | (375) 555-8161 | NULL            | 4V16VO0       |
-- | 985497 | Deborah | (344) 555-9601 | 8714200946      | 10I5658       |
-- +--------+---------+----------------+-----------------+---------------+

SELECT * FROM flights WHERE day = 29 AND month = 7 AND origin_airport_id IN (SELECT id FROM airports WHERE city = 'Fiftyville'); -- 5 flight on 29th from Fiftyville
SELECT city FROM airports WHERE id IN (SELECT destination_airport_id FROM flights WHERE destination_airport_id = 4); -- earliest flight on 29th was taken to NYC

SELECT * FROM people WHERE id IN (SELECT person_id FROM bank_accounts WHERE account_number IN (SELECT account_number FROM atm_transactions WHERE day = 28 AND month = 7 AND atm_location = 'Leggett Street')) AND license_plate IN (SELECT license_plate FROM bakery_security_logs WHERE month = 7 AND day = 28 AND hour = 10 AND minute <= 25 AND activity = 'exit') AND phone_number IN (SELECT caller FROM phone_calls WHERE day = 28 AND month = 7 AND duration <= 60) AND passport_number IN (SELECT passport_number FROM passengers WHERE flight_id IN (SELECT id FROM flights WHERE day = 29 AND month = 7 AND hour = 8 AND origin_airport_id IN (SELECT id FROM airports WHERE city = 'Fiftyville')));
-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate | Suspect is Bruce, as he is taking earliest flight
-- +--------+-------+----------------+-----------------+---------------+ Thief Bruce Found!
-- | 686048 | Bruce | (367) 555-5533 | 5773159633      | 94KL13X       |
-- +--------+-------+----------------+-----------------+---------------+

SELECT * FROM phone_calls WHERE day = 28 AND month = 7 AND duration <= 60 AND caller = '(367) 555-5533';
-- +-----+----------------+----------------+------+-------+-----+----------+
-- | id  |     caller     |    receiver    | year | month | day | duration | call between thief and accomplice
-- +-----+----------------+----------------+------+-------+-----+----------+
-- | 233 | (367) 555-5533 | (375) 555-8161 | 2024 | 7     | 28  | 45       |
-- +-----+----------------+----------------+------+-------+-----+----------+

-- +--------+-------+----------------+-----------------+---------------+
-- |   id   | name  |  phone_number  | passport_number | license_plate | Accomplice Found!
-- +--------+-------+----------------+-----------------+---------------+
-- | 864400 | Robin | (375) 555-8161 | NULL            | 4V16VO0       |
-- +--------+-------+----------------+-----------------+---------------+
