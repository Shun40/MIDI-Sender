import mido

class MidiEvent:
    """
    MIDIイベント(MIDIメッセージとデルタタイムの組)のクラス
    """
    def __init__(self, message, time):
        """
        コンストラクタ

        Parameters
        ----------
        message : list
            ステータスバイト, データバイト1, データバイト2から成るリスト
        time : int
            デルタタイム
        """
        self.message = message
        self.time = time


class MidiEvents(list):
    """
    Midiイベント群のクラス
    """
    def __init__(self, path):
        """
        コンストラクタ

        Parameters
        ----------
        path : str
            MIDIファイルのファイルパス
        """
        list.__init__(self)
        self.get_events_from_file(path)


    def get_events_from_file(self, path):
        """
        MIDIファイルを読み込みMIDIイベント群を取得する

        Parameters
        ----------
        path : str
            MIDIファイルのファイルパス
        """
        events = mido.MidiFile(path)
        for event in events:
            message = event.bytes()
            time = event.time
            self.append(MidiEvent(message, time))


    def to_abs_time(self):
        """
        全MIDIイベントのデルタタイム(相対時間)を累積時間(絶対時間)に変換する
        (e1, 0.5), (e2, 1.0), (e3, 0.5) --> (e1, 0.5), (e2, 1.5), (e3, 2.0)
        """
        for index in range(1, len(self)):
            self[index].time += self[index - 1].time


    def to_rel_time(self):
        """
        全MIDIイベントの累積時間(絶対時間)をデルタタイム(相対時間)に変換する
        (e1, 0.5), (e2, 1.5), (e3, 2.0) --> (e1, 0.5), (e2, 1.0), (e3, 0.5)
        """
        for index in range(len(self) - 1, 0, -1):
            self[index].time -= self[index - 1].time


    def pop_events_in_time(self, time):
        """
        送信時刻が指定時間以下のMIDIイベントを取得し, リストから削除する

        Parameters
        ----------
        time : float
            ターゲット時間
        """
        events_in_time = [event for event in self if event.time <= time]
        # 取り出したイベントを元のリストから消す
        for event in events_in_time:
            self.remove(event)
        return events_in_time


    def show(self):
        """
        全MIDIイベントを表示する
        """
        print('> | time, status, data1, data2')
        for event in self:
            time = event.time # タイム
            status = event.message[0] # ステータスバイト
            data1 = event.message[1] # データバイト1
            data2 = event.message[2] # データバイト2
            print('> | {:.3f}, {}, {}, {}'.format(time, status, data1, data2))
