sillystream
---

sillystream sends anything passed to sillystream.server.write to all clients
connected to the sillystream.server.
It is especially useful for daemon processes.

Docker building and pushing using sillystream to see output
of remote daemon [blog post](http://pdxjohnny.github.io/2015/07/24/gitlab-automated-docker-builds.html)

![sillystream-docker](https://raw.githubusercontent.com/pdxjohnny/sillystream/master/examples/docker.gif)

Using sillystream in python, more in examples folder

```python
import sys
import time
import sillystream

# Number to print to
GO_TO = 50

# Create sillystream server
output = sillystream.server()
# Start the server
output.start_thread()
# Set stdout and stderr to sillystream server
sys.stdout = output
sys.stderr = output

# Print numbers
for num in range(0, GO_TO):
    print(num)
    time.sleep(0.5)
```

Then in another shell to see the output

```bash
python -m sillystream client
```
