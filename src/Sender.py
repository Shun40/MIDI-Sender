from rtmidi.midiutil import open_midiport
import schedule
import time, datetime, copy
from Midi import MidiEvent

class Sender:
    """
    MIDIイベントの送信の機能をまとめたクラス
    """
    def __init__(self):
        """
        コンストラクタ
        """
        self.midi_out, self.port = open_midiport(None, "output", client_name = 'sender')
        self.events = [] # 送信したMIDIイベントの情報
        self.index = 0 # 次に送るMIDIイベントのインデックス


    def send_message(self, message):
        """
        MIDIメッセージを送信する

        Parameters
        ----------
        message : list
            送りたいMIDIメッセージ
        """
        self.midi_out.send_message(message)
        self.events.append(MidiEvent(message, datetime.datetime.now())) # append() : O(1)


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
        # 各MIDIメッセージの送信時刻(絶対時間)を計算する
        events.to_abs_time()

        # interval[sec]間隔でMIDIメッセージ送信を実行するようスケジューラを設定
        schedule.every(interval).seconds.do(self.send_events_in_time, events, time.time())

        # MIDIイベントをすべて送信するまでループ実行
        while self.index != len(events):
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
        # 経過時間を計算
        elapsed_time = time.time() - start_time

        # 送信時刻が経過時間以下のMIDIイベントを取得
        events_in_time = []
        for index in range(self.index, len(events)):
            if events[index].time <= elapsed_time:
                events_in_time.append(events[index]) # append() : O(1)
            else:
                break

        # 取得したMIDIイベントを送信
        for event in events_in_time:
            self.send_message(event.message)

        # 次に送るMIDIイベントのインデックスを更新
        self.index += len(events_in_time)


    def show_send_events_and_times(self):
        """
        送信したMIDIイベントと送信時刻を表示する
        """
        for event in self.events:
            print('MIDI OUT : {} @ {}'.format(event.message, event.time))


    def close_midi_out(self):
        """
        MIDI OUTポートを閉じる
        """
        self.midi_out.close_port()
