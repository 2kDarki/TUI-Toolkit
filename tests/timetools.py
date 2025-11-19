from datetime import datetime as dt, timedelta
from tuikit.exceptions import TimeError
from tuikit import timetools
import unittest
import time

class TestTimeTools(unittest.TestCase):
    def setUp(self):
        self.fixed_now = timetools.EIGHTEENTH
        self.convert   = timetools.convert
        self.gtl       = timetools.get_time_lapsed
        self.cargs     = ["01", "01:30", "01:30:30"]

    def test_convert_hours(self):
        expect  = [1, 1.5, 1.5083333333333333]
        for arg, exp in zip(self.cargs, expect):
            self.assertEqual(self.convert(arg), exp)       

    def test_convert_minutes(self):
        m      = "minutes"
        expect = [60, 90, 90.5]
        for arg, exp in zip(self.cargs, expect):
            self.assertEqual(self.convert(arg, m),exp)

    def test_convert_seconds(self):
        s      = "seconds"
        expect = [3600, 5400, 5430]
        for arg, exp in zip(self.cargs, expect):
            self.assertEqual(self.convert(arg, s),exp)
            
    def test_convert_invalid_format(self):
        with self.assertRaises(TimeError):
             self.convert("24:00", "hours")
        with self.assertRaises(TimeError):
             self.convert("12:60", "minutes")
        with self.assertRaises(TimeError):
             self.convert("12:30:60", "seconds")
        with self.assertRaises(TimeError):
             self.convert("not-a-time", "hours")
        with self.assertRaises(TimeError):
             self.convert("12:30", "lightyears")

    def test_get_unit_limits(self):
        gul      = timetools.get_unit_limits
        plural   = ["seconds", "minutes", "hours"]
        singular = [i[:-1] for i in plural]
        limits   = [60, 60, 24]
        
        for case in [True, False]:
            exp = plural if case else singular, limits
            self.assertEqual(gul("hour", case), exp)
        
        with self.assertRaises(TimeError):
            gul("centaur")        
            
    def test_timestamp(self):
        stamp  = timetools.timestamp 
        time   = "2007-03-23T13:15"
        exp    = [
            "Friday, 23 March 2007 • 13:15",
            "Friday, 23 March 2007",
            "23 Mar 2007",
            "2007/03/23"
        ]
        
        self.assertEqual(stamp(time        ), exp[0])
        self.assertEqual(stamp(time,      1), exp[1])
        self.assertEqual(stamp(time,   0, 1), exp[2])
        self.assertEqual(stamp(time, mini=1), exp[3])
        with self.assertRaises(TimeError):
            timetools.timestamp("invalid-date")

    def test_format_time_string(self):
        fmt    = timetools.format_time_string
        args   = [[2, "days"], [0, "days"], 
                 [[1, "day"], [2, "hours"]], 
                 (3, "minutes")]
        tense  = ["past", "future", None, "future"]
        expect = ["2 days ago", "just now",
                  "1 day and 2 hours", "in 3 minutes"]
        
        for arg, t, exp in zip(args, tense, expect):
            f, s = arg
            self.assertEqual(fmt(f, s, tense=t), exp)
        
    def test_format_unit(self):
        out, major = timetools.format_unit(130, 60, 
                     "hour", "minute", tense="past")
                     
        self.assertEqual(out, "2 hours and 10 "
                             +"minutes ago")
        self.assertEqual(major, 2)
   
    def test_get_time_lapsed_fuzzy(self):
        past   = (self.fixed_now - timedelta(days=365 
               * 2)).isoformat()
        result = self.gtl(past, _fixed=True)
        self.assertIn("2 years", result)

    def test_get_time_lapsed_raw(self):
        past   = (self.fixed_now - timedelta(seconds
               = 7200)).isoformat()
        result = self.gtl(past, fuzzy=False, _fixed
               = True)
        self.assertAlmostEqual(result, 7200, delta=1)

    def test_get_time_lapsed_numeric(self):
        result = self.gtl(31536000 * 3, fuzzy=False, 
                 num=True)
        self.assertEqual(result, 87091200)
       
    def test_to_iso(self):
        iso = timetools.to_iso
        now = dt.now()
        arg = [now, "2007-03-23"]
        exp = [now.isoformat(), "2007-03-23T00:00:00"]
        
        for a, e in zip(arg, exp):
            self.assertEqual(iso(a), e)
    
    def test_format_time(self):
        fmt_time  = timetools.format_time
        args      = [2, -30, 10, -90]
        unit      = ["hour", "minute"]
        tense     = [None, None, "future"]
        exp       = ["2 hours", "30 minutes ago", 
                    "in 10 minutes", "ago"]
        
        for a, u, t, e in zip(args, unit, tense, exp):
            result = fmt_time(a, u, tense=t)
            self.assertIn(e, result)
             
        result = fmt_time(1.51, set_to="hour",
                 faulty=False)
        units = ["hour", "minutes", "seconds"]
        for unit in units: self.assertIn(unit, result)         
        
        with self.assertRaises(TimeError):
             fmt_time(1, set_to="fortnight")

        with self.assertRaises(TimeError):
             fmt_time("soon", set_to="minute")
             
        with self.assertRaises(TimeError):
             fmt_time(5, tense="later")
        
    def test_time_lapsed_just_now(self):
        lapsed = timetools.time_lapsed
        args = [0.5, 15, 120, -10]
        exp  = ["Just now", "15 seconds ago",
               "2 minutes", "Tempered"]
        
        for i, (arg, e) in enumerate(zip(args, exp)):
            if i < 2:
                self.assertEqual(lapsed(arg), e)
                continue
            result = lapsed(arg)
            self.assertIn(e, result)

    def test_get_age(self):
        age    = timetools.get_age
        cases  = [True, False]
        years  = [y for y in range(2000, 2024)] 
        ages   = [a for a in range(2,26)][::-1]
        
        for case in cases:
            for a, year in zip(ages, years):
                y = f"{year}-03-23"
                if not case: a = f"{a} years"
                self.assertEqual(age(y, case, 1), a)
            
        with self.assertRaises(TimeError):
            timetools.get_age("not-a-date")
    
    def test_clock(self):
        clock = timetools.clock
        args  = [13.5, 1.255, 1.25]
        tion  = ["24", "24", "12"]
        mer   = [None, None, "a.m.", "p.m"]
        exp   = ["13:30", "01:15:18", "01:15","13:15"]
        
        for a, t, m, e in zip(args, tion, mer, exp):
            self.assertEqual(clock(a, t, m), e)

        with self.assertRaises(TimeError):
            timetools.clock(1.25, "12", "midnight")

        with self.assertRaises(TimeError):
            timetools.clock(1.25, "13")