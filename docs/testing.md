
# Testing The Rpggen Code

This describes how to run tests and also how to write new tests.

# Running Tests (and Understanding Output)

    cd tests
    ./testall

This should run all the unittests first and then all the visual tests.
Each unittest should print out an "OK" right after the number of tests it ran.
Each visual test should print out some text, which you should examine.  It should make sense, and there should not be any error messages.

# Writing Tests

There are two types of tests in the test suite:
1. Unittests
2. Visual Tests

If possible, please write unittests.  Only use visual tests to test things where the output is random, and unittest just can't be used.

## Writing Unittests

* In general, follow the examples that are already there, especially by using the unittest framework.
* These files should always start with a t_*.
* Your test cases should generate no output (or very little output), as the unittest library will generate standard success/failure output.
* The Rpggen.testData = 2 code will cause "random" rolls to all be 2, and is very helpful for generating the same result each time.  The exact number is not important.  You can use anything from 1-6 for your tests.
* The unittest framework is easy to learn and does include methods for testing function calls that result in exceptions, and many other situations.

## Writing Visual Tests

* In general, follow the examples that are already there.
* These files should always start with a th_*.
* These tests should generate one page of output, no more.  (And use your best judgement as to how big a page is).
* It should be obvious to anyone looking at the output if an error has occured.  These tests should never write error-looking text if no error has occured, and should always print out an obvious error message, if an error does occure.
* Add new tests to the testall.bat command at the end of the ht_* list.