import math

input_file = "matched_courses.jsonl"
output_template = "2025_course_data/cs_corpus_part_{:02}.jsonl"
num_files = 7

# Count total lines
with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

total_lines = len(lines)
chunk_size = math.ceil(total_lines / num_files)

for i in range(num_files):
    start = i * chunk_size
    end = min((i + 1) * chunk_size, total_lines)
    chunk_lines = lines[start:end]

    output_file = output_template.format(i + 1)
    with open(output_file, "w", encoding="utf-8") as f_out:
        f_out.writelines(chunk_lines)

    print(f"✅ Wrote {len(chunk_lines)} lines to {output_file}")
