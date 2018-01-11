## Please follow the guide below

- Issues submitted without this template format will be **ignored**.
- You will be asked some questions and requested to provide some information, please read them **carefully** and answer completely.
- Put an `x` into all the boxes [ ] relevant to your issue (like so [x]).
- Use the *Preview* tab to see how your issue will actually look like.

---

### Before submitting an issue, make sure you have:
- [ ] Updated to the latest version
- [ ] Read the [README](https://github.com/instagrambot/instabot/blob/master/README.md) and [docs](https://github.com/instagrambot/instabot/tree/master/docs)
- [ ] [Searched](https://github.com/instagrambot/instabot/search?type=Issues) the bugtracker for similar issues including **closed** ones

### Purpose of your issue?
- [ ] Bug report (encountered problems/errors)
- [ ] Feature request (request for a new functionality)
- [ ] Question
- [ ] Other

---

### The following sections requests more details for particular types of issues, you can remove any section (the contents between the triple ---) not applicable to your issue.

---

### For a *bug report*, you **must** include the Python version used, *code* that will reproduce the error, and the *error log/traceback*.

Paste the output of ``python -V`` here:

Code:

```python
# Example code that will produce the error reported
from instabot import Bot

bot = Bot()
bot.login(username="user", password="pass")
followers = bot.get_user_followers(bot.user_id)
```

Error/Debug Log:

```python
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: integer division or modulo by zero
```


---

### Describe your issue

Explanation of your issue goes here. Please make sure the description is worded well enough to be understood with as much context and examples as possible.
