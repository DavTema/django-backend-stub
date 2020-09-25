from multiprocessing import cpu_count

bind = '0.0.0.0:8000'
workers = cpu_count() * 2 + 1
timeout = 60
graceful_timeout = 60
keepalive = 75
worker_class = 'sync'
worker_tmp_dir = '/dev/shm'
