from datetime import datetime as dt

class DayOfWeek:

  def getShort(day_int: int):
    days_of_week = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
    return days_of_week[day_int]
  
  def getShort(date : dt):
    day_int = date.weekday()
    days_of_week = ["MON","TUE","WED","THU","FRI","SAT","SUN"]
    return days_of_week[day_int]
  
  def getLong(day_int: int):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days_of_week[day_int]
  
  def getLong(date : dt):
    day_int = date.weekday()
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return days_of_week[day_int]