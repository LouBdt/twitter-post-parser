# twitter-post-parser
Python script that is to be used after parsing your twitter archive with Tim Hutton's archive parser :https://github.com/timhutton/twitter-archive-parser.

=========How to use it=========

Once you have downloaded your twitter archive, follow instructions at https://github.com/timhutton/twitter-archive-parser/blob/main/README.md

Once you have run it you should have a folder with different files:
- DATE-Tweet-Archive-DATE.html
- DATE-Tweet-Archive-DATE.md
- DMs-Archive-USER.md
- followers.txt
- following.txt
And the folders:
- assets
- data
- media

This script only reads the second type of file (DATE-Tweet-Archive-DATE.md), the ones containing all your tweets (it doesn't open anything else).

To use the script, simply right click on the following link >>https://github.com/LouBdt/twitter-post-parser/blob/a539650a769991fb4fc7e7e8a59bf0c65819dbe4/postparserforthreads.py<< and "save link as..." and save it in the folder where the first program extracted all the .md and .html files.

Then run the script by openning a terminal in this folder and type something like "python3 postparserforthreads.py".
You'll have to input the username of the account whose archive you're analysing
The script will do its thing.
Then it will ask permission to clear the /Result folder it will create. If this folder already exists for some reason and you type "y", it will be erased. 
After saving the results, you will have a folder named "/Result" that was created, containing a .txt file named stats.txt. 
You will also have a folder named "/Threads" where all your threads (of 2 tweets and more) are saved with the number of tweets in it and the date of the first tweet.
