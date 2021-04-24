
def is_valid_task_no(s, page_no, total_no_of_tasks):
    try:
        val = int(s)
        end = min(total_no_of_tasks, (page_no) * 5)
        last_task = end % 5 if end % 5 != 0 else 5
        if 1 <= val <= total_no_of_tasks:
            return True
    except ValueError:
        return False