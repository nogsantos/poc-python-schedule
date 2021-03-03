import schedule
import pytest

from unittest.mock import patch, PropertyMock
from freezegun import freeze_time

from run import AppScheduler


@pytest.fixture
def scheduler():
    yield AppScheduler()


@pytest.fixture
def service():
    schedule.clear()
    AppScheduler.RUNNING = PropertyMock(side_effect=[1, 0])
    yield AppScheduler()


@patch("run.AppScheduler.add_schedules")
@patch("run.schedule.run_pending")
def test_scheduler_called_add_run_pending(run_pending, add_schedules, service):
    service.runner()

    run_pending.assert_called_once()
    add_schedules.assert_called_once()


@patch("run.AppScheduler.dispatch")
def test_scheduler_default(dispatch, scheduler):
    scheduler.event(
        event_type="process.every.day.minuts",
        service_name="scheduler",
        event_data={"some_data": "default"},
    )

    dispatch.assert_called_once()


@freeze_time("2020-01-01 00:00:00")
@patch("run.AppScheduler.dispatch")
def test_scheduler_at_specific_day_1(dispatch, scheduler):
    scheduler.event(
        event_type="process.every.day.minuts",
        service_name="scheduler",
        event_data={"some_data": "in especific day"},
        days=[1, 2, 3],
    )

    dispatch.assert_called_once()


@freeze_time("2020-01-02 00:00:00")
@patch("run.AppScheduler.dispatch")
def test_scheduler_at_specific_day_2(dispatch, scheduler):
    scheduler.event(
        event_type="process.every.day.minuts",
        service_name="scheduler",
        event_data={"some_data": "in especific day"},
        days=[1, 2, 3],
    )

    dispatch.assert_called_once()


@freeze_time("2020-01-04 00:00:00")
@patch("run.AppScheduler.dispatch")
def test_scheduler_not_called_at_day_out_of_range(dispatch, scheduler):
    scheduler.event(
        event_type="process.every.day.minuts",
        service_name="scheduler",
        event_data={"some_data": "in especific day"},
        days=[1, 2, 3],
    )

    dispatch.assert_not_called()
