# my_interface
a interface 

### Functional:
the files are the interface program for request the data of region count, queue length, flow count from the analysis daemon of intelligent video, it also listens the alarm data from the daemon, such crossboundary, endplatform,etc.

---
### ENVS:
linux+python3
while, under windows(as the multiprocessing mechanisms under linux and windows are different, so the codes should be made a little change)


----
### Protocols used in:
FTP(for images transmission)+HTTP(for the transmission of alarm data)

---
### TOOLS:
Falsk(http request and response)+MySQL(data store)

----
### others:
multiprocessing + multithreading + mutexlock(in threading)

