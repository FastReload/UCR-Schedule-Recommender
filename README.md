# UCR Course Data Preprocessing Pipeline

This branch contains scripts for processing UCR course data for the RAG corpus.

## Scripts:
- **split.py**: Splits matched courses into multiple JSONL files
- **jsonl_test.py**: Preprocesses course data for RAG corpus
- **course_filter.py**: Filters and categorizes courses by CS degree requirements  
- **convert.py**: Converts JSON to JSONL format
- **combine.py**: Combines multiple course data JSON files

## Usage:
Run scripts in order: combine.py → convert.py → course_filter.py → jsonl_test.py → split.py
