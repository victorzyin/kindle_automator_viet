### What does this script do?

Automatically add vietnamese books from the website www.sachhoc.com into your Kindle E-Reader

### How does it work?

It scrapes a [page](https://sachhoc.com/ngon-tinh?page=3&init=TU1FZTNPYzlKT3ZRU0MyN1NVZlFHQT09).

The script then opens all the Google Drive links individually with selenium and bs4. 

Then it downloads the pdfs.

Finally, it emails the result to the Kindle E-Reader (which shows up in your library upon sync).

### How can I use this?

Install the python dependencies, put your info into input.yaml. Create a burner email with 2-factor auth on, and setup [custom email app password](https://stackoverflow.com/questions/72478573/how-to-send-an-email-using-python-after-googles-policy-update-on-not-allowing-j) That's it!

[How to find your Kindle email](https://www.amazon.com/sendtokindle/email)
