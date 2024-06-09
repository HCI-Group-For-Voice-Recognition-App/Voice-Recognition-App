"""输入的音频文件（WAV格式）分割成多个较小的音频文件"""
import wave
import os


def split_audio(filename, chunk_length=2, max_chunks=4, input_dir='samples', output_dir='samples'):
    input_path = os.path.join(input_dir, filename + '.wav')
    try:
        orig_audio = wave.open(input_path, 'r')
    except FileNotFoundError:
        print("文件 samples\\{}.wav 未找到。".format(filename))
        return
    except wave.Error as e:
        print("无法打开文件 samples\\{}.wav: {}".format(filename, e))
        return

    frame_rate = orig_audio.getframerate()  # 获取帧率
    n_channels = orig_audio.getnchannels()  # 获取声道数
    samp_width = orig_audio.getsampwidth()  # 获取采样宽度

    try:
        for i in range(max_chunks):
            start = 1 + i * chunk_length
            end = start + chunk_length
            print("正在处理第 {} 段: 开始 {} 秒, 结束 {} 秒".format(i + 1, start, end))

            orig_audio.setpos(start * frame_rate)
            chunk_data = orig_audio.readframes(int((end - start) * frame_rate))

            output_filename = "{}_cut_{}.wav".format(filename, i)
            output_path = os.path.join(output_dir, output_filename)
            with wave.open(output_path, 'w') as chunk_audio:
                chunk_audio.setnchannels(n_channels)
                chunk_audio.setsampwidth(samp_width)
                chunk_audio.setframerate(frame_rate)
                chunk_audio.writeframes(chunk_data)

            print("第 {} 段已保存为 {}".format(i + 1, output_path))
    except wave.Error as e:
        print("处理音频时出错: {}".format(e))
    finally:
        orig_audio.close()
        print("原始音频文件已关闭。")


if __name__ == "__main__":
    filename = input()
    split_audio(filename)
