from rtmidi.midiutil import open_midiport
import schedule
import time, datetime, copy

class Sender:
    """
    MIDIイベントの送信の機能をまとめたクラス
    """
    def __init__(self):
        """
        コンストラクタ
        """
        self.midi_out, self.port = open_midiport(None, "output", client_name = 'sender')
        self.events = []
        self.times = []


    def send_message(self, message):
        """
        MIDIメッセージを送信する

        Parameters
        ----------
        message : list
            送りたいMIDIメッセージ
        """
        self.midi_out.send_message(message)
        self.times.append(datetime.datetime.now()) # append() : O(1)


    def send_events(self, events, interval):
        """
        MIDIイベント群を送信する

        Parameters
        ----------
        events : MidiEvents
            送りたいMIDIイベント群
        interval : float
            ループ間隔の値[sec]
        """
        self.events = copy.copy(events)

        # 各MIDIメッセージの送信時刻(絶対時間)を計算する
        events.to_abs_time()

        # interval[sec]間隔でMIDIメッセージ送信を実行するようスケジューラを設定
        schedule.every(interval).seconds.do(self.send_events_in_time, events, time.time())

        # MIDIイベントをすべて送信するまでループ実行
        while events:
            schedule.run_pending()

        self.close_midi_out()


    def send_events_in_time(self, events, start_time):
        """
        送信時刻が経過時間以下のMIDIイベントを送信する

        Parameters
        ----------
        events : MidiEvents
            送りたいMIDIイベント群
        start_time : float
            MIDIシーケンスの送信開始時刻
        """
        # 送信時刻が経過時間以下のMIDIイベントをすべて送信する
        events_in_time = events.pop_events_in_time(time.time() - start_time)
        for event in events_in_time:
            self.send_message(event.message)


    def show_send_events_and_times(self):
        """
        送信したMIDIイベントと送信時刻を表示する
        """
        for index in range(len(self.events)):
            event = self.events[index]
            time = self.times[index]
            print('MIDI OUT : {} @ {}'.format(event, time))


    def close_midi_out(self):
        """
        MIDI OUTポートを閉じる
        """
        self.midi_out.close_port()
