import sys, os, argparse
from Midi import MidiEvents
from Sender import Sender

MILLI_SEC = 0.001
MICRO_SEC = 0.000001

# ループ間隔のデフォルト値[sec]
DEFAULT_INTERVAL = 2.0 * MILLI_SEC

def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file', help = 'MIDI file path (*.mid)', required = True, type = str)
    parser.add_argument('-i', '--interval', help = 'Interval time [sec]', default = DEFAULT_INTERVAL, type = float)

    return parser.parse_args()


def main():
    args = get_args()

    path = args.file
    interval = args.interval

    if not os.path.exists(path):
        print('{} does not exist.'.format(path))
        sys.exit(1)

    events = MidiEvents(path)

    sender = Sender()
    sender.send_events(events, interval)
    sender.show_send_events_and_times()


if __name__ == '__main__':
    main()
