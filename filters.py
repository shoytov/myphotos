from datetime import datetime
from init import app


@app.template_filter()
def my_strftime(value: datetime):
	return value.strftime('%d.%m.%Y')