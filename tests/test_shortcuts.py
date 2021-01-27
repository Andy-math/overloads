import math
from typing import Any

import numpy
from overloads import shortcuts


# save_load 支持树状路径
class Test_save_load_check():
    def test_普通SL(self) -> None:
        a = [{()}]
        filename = 'a.pkl'
        shortcuts.save(filename, a)
        assert shortcuts.load(filename) == a

    def test_新建不存在的路径(self) -> None:
        a = [{()}]
        filename = 'a/a/a/a/a.pkl'
        shortcuts.save(filename, a)
        assert shortcuts.load(filename) == a

    def test_覆盖重复的路径(self) -> None:
        a = [{()}]
        filename = 'a/a/a/a/a.pkl'
        shortcuts.save(filename, a)
        assert shortcuts.load(filename) == a


# 时间戳
class Test_时间戳检查():
    def test_时间戳行为预期(self) -> None:
        import datetime
        ss = shortcuts.timestamp()
        assert isinstance(datetime.datetime.strptime(ss, '%Y_%m_%d %H.%M.%S'), datetime.datetime)

    def test_时间戳时间准确性(self) -> None:
        import datetime
        now = datetime.datetime.now()
        ss = shortcuts.timestamp(time=now)
        assert shortcuts.timestamp(time=datetime.datetime.strptime(ss, '%Y_%m_%d %H.%M.%S')) == ss

    def test_时间戳自定义格式(self) -> None:
        import datetime
        fmt = '%Y.%m.%d %H_%M_%S'
        now = datetime.datetime.now()
        ss = shortcuts.timestamp(time=now, format=fmt)
        assert shortcuts.timestamp(time=datetime.datetime.strptime(ss, fmt), format=fmt) == ss


def cap_except(f: Any) -> AssertionError:
    try:
        f()
        assert False
    except AssertionError as e:
        return e


# assertInfNaN
class Test_assertInfNaN():
    def test_输入正无穷(self) -> None:
        ss = '出现了Inf或NaN'
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN(numpy.array([numpy.inf]))).args[0][0] == ss
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN(numpy.array([math.inf]))).args[0][0] == ss

    def test_输入负无穷(self) -> None:
        ss = '出现了Inf或NaN'
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN(numpy.array([-numpy.inf]))).args[0][0] == ss
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN(numpy.array([-math.inf]))).args[0][0] == ss

    def test_输入NaN(self) -> None:
        ss = '出现了Inf或NaN'
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN(numpy.array([numpy.nan]))).args[0][0] == ss
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN(numpy.array([math.nan]))).args[0][0] == ss


# assertInfNaN_float
class Test_assertInfNaN_float():
    def test_输入正无穷(self) -> None:
        ss = '出现了Inf或NaN'
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN_float(numpy.inf)).args[0][0] == ss
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN_float(math.inf)).args[0][0] == ss

    def test_输入负无穷(self) -> None:
        ss = '出现了Inf或NaN'
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN_float(-numpy.inf)).args[0][0] == ss
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN_float(-math.inf)).args[0][0] == ss

    def test_输入NaN(self) -> None:
        ss = '出现了Inf或NaN'
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN_float(numpy.nan)).args[0][0] == ss
        assert cap_except(
            lambda: shortcuts.assertNoInfNaN_float(math.nan)).args[0][0] == ss
