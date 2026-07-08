
# Sample prompt

I'd like to have a blog system using sqlite as db, please have a simple register, login system, only allow logined user to post,. write a proposal.md, archtirecutre.md, and design.md first. let me review. put all those .md under web/python_sqlite

Let according to these documnt, implement the MVP under web/python_sqlite dir.

Please use python flask, sqlite stack
add README.md, so people know how to get started

please add test utility as well to make sure it will not regerss in the future

Note:
to be able to deploy on comrite cloud, you need to
Write a code to use `COMRITE_CLOUD_DATA_VOLUME` enviroment value to get data dir.

The path where persistent storage is mounted inside your container. Use this to
store uploads, SQLite databases, or any data that should survive restarts.
Default value: `/app/data`

```python
import os

data_dir = os.environ.get("COMRITE_CLOUD_DATA_VOLUME", "/app/data")
db_path = os.path.join(data_dir, "myapp.db")
uploads_dir = os.path.join(data_dir, "uploads")
```
