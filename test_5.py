import whisperx
import gc
import arrow
import os
import requests
import torch
from whisperx import load_align_model, align
from whisperx.diarize import DiarizationPipeline, assign_word_speakers
# import help.amazon_data as had
import loguru

lg = loguru.logger

# 设置代理
proxy = "http://192.168.8.36:1080"
os.environ["http_proxy"] = proxy
os.environ["https_proxy"] = proxy


def make_whisperx_diarization(audio_file, start_time):
    device = "cpu"
    # audio_file = "data/output_2.wav"
    batch_size = 16
    compute_type = "int8"
    lg.info('开始加载模型')
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)

    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)

    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=device)
    result = whisperx.align(result["segments"], model_a, metadata, audio, device, return_char_alignments=False)

    diarize_model = whisperx.DiarizationPipeline(use_auth_token="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", device=device)

    diarize_segments = diarize_model(audio)
    # diarize_model(audio, min_speakers=min_speakers, max_speakers=max_speakers)

    result = whisperx.assign_word_speakers(diarize_segments, result)

    # print(diarize_segments)
    # print(result["segments"])  # segments are now assigned speaker IDs
    lg.info(f'语音识别结束，开始识别说话人')
    speaker_a = assign_word_speakers(diarize_segments, result)
    lg.info(f'识别成功，开始保存到数据库中')
    make_data(speaker_a, start_time)
    lg.info(f'保存完毕')


def assign_speakers(
        diarization_result, aligned_segments):
    """
    Assign speakers to each transcript segment based on the speaker diarization result.

    Args:
        diarization_result: Dictionary representing the diarized audio file, including the speaker embeddings and the number of speakers.
        aligned_segments: Dictionary representing the aligned transcript segments.

    Returns:
        A list of dictionaries representing each segment of the transcript, including the start and end times, the
        spoken text, and the speaker ID.
    """
    result_segments, word_seg = assign_word_speakers(
        diarization_result, aligned_segments["segments"]
    )
    results_segments_w_speakers = []
    for result_segment in result_segments:
        results_segments_w_speakers.append(
            {
                "start": result_segment["start"],
                "end": result_segment["end"],
                "text": result_segment["text"],
                "speaker": result_segment["speaker"],
            }
        )
    return results_segments_w_speakers


def make_data(result, start_time):
    data_list = []
    for segment in result["segments"]:
        data = {}
        now = arrow.get(start_time)
        start = now.shift(seconds=segment["start"]).format("YYYY-MM-DD HH:mm:ss")
        end = now.shift(seconds=segment["end"]).format("YYYY-MM-DD HH:mm:ss")
        print("【" + start + "->" + end + "】" + segment["speaker"] + "：" + segment["text"])
        data['StartTime'] = start
        data['EndTime'] = end
        data['Time'] = f"{start}--{end}"
        data['Speaker'] = segment["speaker"]
        data['Content'] = segment["text"]
        data_list.append(data)
    # had.insert_batch_data(data_list, 'speaker_diarization')


if __name__ == '__main__':
    start_time = "2023-11-22 09:03:00"
    audio_file = "data/output2.wav"
    make_whisperx_diarization(audio_file, start_time)

# import whisperx
# import os
# import arrow
# import loguru
# import help.amazon_data as had
#
#
# class WhisperXDiarization:
#     def __init__(self, device="cpu", batch_size=16, compute_type="int8", proxy=None):
#         self.device = device
#         self.batch_size = batch_size
#         self.compute_type = compute_type
#         self.proxy = proxy
#         if proxy:
#             os.environ["http_proxy"] = proxy
#             os.environ["https_proxy"] = proxy
#         self.logger = loguru.logger
#         self.model = self.load_model()
#
#     def load_model(self):
#         self.logger.info('开始加载模型')
#         return whisperx.load_model("large-v2", self.device, compute_type=self.compute_type)
#
#     def make_whisperx_diarization(self, audio_file, start_time):
#         audio = whisperx.load_audio(audio_file)
#         result = self.model.transcribe(audio, batch_size=self.batch_size)
#
#         model_a, metadata = whisperx.load_align_model(language_code=result["language"], device=self.device)
#         result = whisperx.align(result["segments"], model_a, metadata, audio, self.device, return_char_alignments=False)
#
#         diarize_model = whisperx.DiarizationPipeline(use_auth_token="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",
#                                                      device=self.device)
#
#         diarize_segments = diarize_model(audio)
#         result = whisperx.assign_word_speakers(diarize_segments, result)
#
#         self.logger.info(f'语音识别结束，开始识别说话人')
#         speaker_a = self.assign_speakers(diarize_segments, result)
#         self.logger.info(f'识别成功，开始保存到数据库中')
#         self.make_data(speaker_a, start_time)
#         self.logger.info(f'保存完毕')
#
#     def assign_speakers(self, diarization_result, aligned_segments):
#         result_segments, word_seg = whisperx.assign_word_speakers(diarization_result, aligned_segments["segments"])
#         results_segments_w_speakers = []
#         for result_segment in result_segments:
#             speaker = result_segment.get('speaker', 'Unknown')  # Assign a default speaker if 'speaker' field is missing
#             results_segments_w_speakers.append({
#                 "start": result_segment["start"],
#                 "end": result_segment["end"],
#                 "text": result_segment["text"],
#                 "speaker": speaker,
#             })
#         return results_segments_w_speakers
#
#     def make_data(self, result, start_time):
#         data_list = []
#         for segment in result["segments"]:
#             now = arrow.get(start_time)
#             start = now.shift(seconds=segment["start"]).format("YYYY-MM-DD HH:mm:ss")
#             end = now.shift(seconds=segment["end"]).format("YYYY-MM-DD HH:mm:ss")
#             print("【" + start + "->" + end + "】" + segment["speaker"] + "：" + segment["text"])
#             data = {
#                 'StartTime': start,
#                 'EndTime': end,
#                 'Time': f"{start}--{end}",
#                 'Speaker': segment["speaker"],
#                 'Content': segment["text"]
#             }
#             data_list.append(data)
#         had.insert_batch_data(data_list, 'speaker_diarization')
#
#
# if __name__ == '__main__':
#     start_time = "2023-11-22 09:03:00"
#     audio_file = "data/output2.wav"
#     proxy = "http://192.168.8.36:1080"
#     diarizer = WhisperXDiarization(proxy=proxy)
#     diarizer.make_whisperx_diarization(audio_file, start_time)
