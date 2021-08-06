import rumps
import json
import subprocess
import time

rumps.debug_mode(True)


class IproxyBarApp(rumps.App):
    def __init__(self):
        super().__init__(name="IproxyBar", icon="icon.png", quit_button=None)
        self.iproxy_process = None
        with open("config.json", "r") as f:
            config = json.load(f)
            self.LOCAL_PORT = config["LOCAL_PORT"]
            self.DEVICE_PORT = config["DEVICE_PORT"]

    def start_iproxy(self):
        if self.iproxy_process is None:  # didn't have a process in background
            print("Start iproxy now...")
            rumps.notification(title="iproxy Bar", subtitle=None, message="Start iproxy now...", sound=False)
            self.iproxy_process = subprocess.Popen(["iproxy", "4444", "44"],
                                                   stdout=subprocess.PIPE,
                                                   stderr=subprocess.PIPE,
                                                   text=True)
            time.sleep(3)  # wait for error
            process_status = self.iproxy_process.poll()
            if process_status is not None and process_status != 0:
                print(f"error: {self.iproxy_process.stderr.readline()}")
                return False
            return True
        else:
            return False

    def stop_iproxy(self):
        if self.iproxy_process is not None:  # has a process in background
            print("Stop iproxy now...")
            rumps.notification(title="iproxy Bar", subtitle=None, message="Stop iproxy now...", sound=False)
            process_status = self.iproxy_process.poll()
            if process_status is None:  # terminate if still run
                self.iproxy_process.terminate()
            self.iproxy_process = None

    @rumps.clicked("Connect")
    def iproxy_switch(self, sender):
        sender.state = not sender.state
        if sender.state:
            if not self.start_iproxy():
                sender.state = not sender.state
        else:
            self.stop_iproxy()

    @rumps.clicked('Stop and Quit')
    def clean_up_before_quit(self, _):
        print("quit and stop iproxy if running")
        self.stop_iproxy()
        rumps.quit_application()

    def __del__(self):
        print("quit and stop iproxy if running")
        self.stop_iproxy()


if __name__ == "__main__":
    IproxyBarApp().run()
