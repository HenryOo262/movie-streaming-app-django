
def file_iterator(blob, start, end):
    try:
        chunk = blob.download_as_bytes(start=start, end=end)
        # print(len(chunk))
        yield chunk
    except Exception as e:
        print(f"Error downloading file chunk: {e}")
        raise