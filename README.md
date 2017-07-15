# HTT Witch (HTTPw)
HTTP Witch just for making you HTTP header be magical

# How to use

python ./httpw.py  <config path>

Configuration format ( write on plaintext ) :
	
	<listen port> | <remote host>:<remote port> | <payload>
	
Payload format

	[host]		remote host
	
	[port]		remote port
	
	[host_port]	remote host and port
	
	[protocol]	HTTP protocol version
	
	[crlf]		/r/n
	
	[connect]	CONNECT [host_port] [protocol]
	
	[cr]		\n
	
	[lf]		\r
	
	[lrcf]		\n\r
