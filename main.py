#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import webapp2
import jinja2
import os
import string


template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),autoescape=True)

class Handler(webapp2.RedirectHandler):
    def write_form(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**args):
        t=jinja_env.get_template(template)
        return t.render(args)

    def render(self,template,**args):
        self.write_form(self.render_str(template,**args))

class FizzBuzz(Handler):
    def get(self):
        n=self.request.get("n",0)
        if n and n.isdigit():
            n=int(n)
            self.render("form.html",n=n)


months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']


monthesDic=dict((m[:3].lower(),m)for m in months)
def valid_month(month):
    month
    if month :
        short=month[:3].lower()
        return  monthesDic.get(short)

def valid_Day(day):
    if day and day.isdigit() :
        day=int(day)
        if day > 0 and day < 32 :
            return day
def valid_year(year):
    if year and year.isdigit():
          year=int(year)
          if year > 1900 and year < 2016 :
              return year


form="""
<!DOCTYPE HTML>
<html>
<body>
<form method="get" >
   <label>Day<input name="day" type="txt" value="%(day)s"></label>
   <label>Year<input name="year" type="txt" value="%(year)s"></label>
   <label>Month<input name="month"  type="txt" value="%(month)s"></label>
   <input type="hidden" value="eggs" name="food">
       <input type="submit" >

    </form>
    <div style="color:red" >%(error)s </div>

</body>
</html>
"""
class MainHandler(webapp2.RequestHandler):
    def write_form(self,error="",month="",day="",year=""):
        self.response.write(form%{"error":error,"day":day,"month":month,"year":year})
    def get(self):
        self.write_form()

    def post(self):
        user_day = self.request.get("day")
        user_month = self.request.get("month")
        user_year = self.request.get("year")
        day = valid_Day(user_day)
        month = valid_month(user_month)
        year = valid_year(user_year)
        if not (day and month and year):
            self.write_form("Enter Valid Data",user_month,user_day,user_year)
        else:
            self.response.write("OK Done")


class Rot13(Handler):
    def get(self, *args, **kwargs):
        self.render("form.html")
    def post(self):
        value=self.request.get("text")
        if value:
            rot13_str=self.rot13(value)
            self.render("form.html",rot13_str=rot13_str)



    def rot13(self,values):
        temp=""
        for value in values:
            ascii = ord(value)
            if ascii >= 65 and ascii <= 90:
                if ascii + 13 > 90:
                    ascii=ascii - 13
                else:
                    ascii=ascii + 13
            elif ascii >=97 and ascii <= 122 :
                if ascii +13 > 122 :
                    ascii=ascii-13
                else: ascii=ascii+13
            temp+=unichr(ascii)

        return temp


class testform(webapp2.RequestHandler):
    def post(self):
        user_day=self.request.get("day")
        user_month=self.request.get("month")
        user_year=self.request.get("year")
        day =valid_Day(user_day)
        month=valid_month(user_month)
        year=valid_year(user_year)
        if not (day and month and year):
            self.response.write(self.request)
app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/testform',testform),
    ('/FizzBuzz',FizzBuzz),('/rot13',Rot13)
        ], debug=True)


def escape_html(s=''):
    if s :
       for (i,o) in (("<","&gt;"),
                     ('>','&lt;'),
                     ('"','&quot;'),
                     ('&','&amp;')):
           s.replace(i,o)
       return  s

print escape_html("<")
print valid_Day('5')