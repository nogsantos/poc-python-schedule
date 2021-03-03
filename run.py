from datetime import datetime
import logging
import schedule
import time


class AppScheduler:
    RUNNING = True

    def dispatch(
        self, event_type, service_name="scheduler_service", event_data=""
    ):
        logging.info(
            f"Event {event_type} start "
            f"Service {service_name} "
            f"Data {event_data} "
        )

    def event(
        self,
        event_type,
        service_name="scheduler_service",
        event_data="",
        days=None,
    ):
        if days:
            current_day = datetime.now().day
            if current_day in days:
                self.dispatch(event_type, service_name, event_data)
                logging.info(f"Especific day {current_day}")
        else:
            self.dispatch(event_type, service_name, event_data)

    def add_schedules(self):
        schedule.every(3).seconds.do(
            self.event,
            event_type="process.every.3.seconds",
            service_name="scheduler",
            event_data={"some": "data"},
        )

        schedule.every(3).seconds.do(
            self.event,
            event_type="process.every.day.minuts",
            service_name="scheduler",
            event_data={"some_data": "in especific day"},
            days=[1, 2, 3],
        )

    def runner(self):
        logging.basicConfig(
            format="%(asctime)s - %(message)s", level=logging.INFO
        )
        logging.info(f"Schedule started at {datetime.now()}")

        self.add_schedules()

        while self.RUNNING:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    AppScheduler().runner()
