import os


def extract_subtitles(srt_file_path, start_index, end_index):
    # Extracting file name and extension
    file_name, file_extension = os.path.splitext(srt_file_path)

    # Generating output file path with double backslashes
    output_file_path = (
        f"{file_name}_extracted_{start_index}_to_{end_index}{file_extension}"
    )

    extracted_subtitles = []

    with open(srt_file_path, "r", encoding="utf-8") as f:
        reading_subtitles = False

        for line in f:
            if line.strip().isdigit():
                subtitle_index = int(line.strip())
                if start_index <= subtitle_index <= end_index:
                    reading_subtitles = True
                else:
                    reading_subtitles = False
            if reading_subtitles:
                extracted_subtitles.append(line)

    # Write extracted subtitles to the output file
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.writelines(extracted_subtitles)

    return output_file_path
