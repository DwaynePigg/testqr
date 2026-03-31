QUICK GUIDE

Choose ASCII from the main menu, type in your message, and wait about 1 to 20 minutes for the program to finish, depending on the length of your message. (See table below, but beware! You may start reading other technical details.) Then scan the code with your phone or something.

Why would you potentially wait up to 20 minutes for your calculator to generate a QR code that you're just going to scan with your phone? I guess that's up to you, but my two main reasons are:
1) It's cool.
2) You can use this program in combination with other 


ASCII MODE

ALPHANUMERIC MODE

BINARY MODE

To use this mode, you must first store your binary data in list BIN (perhaps with the list editor) and then select Binary encoding. Unlike Alphanumeric and ASCII mode, Binary mode does not prompt you to input the data and assumes list BIN has already been set up.

VERSIONS

This program can create QR codes ranging from version 1 to 11.

| Ver | Size | Binary | AlphaNum | ECC Time | Draw Time | Total Time | Char/sec |
|   1 |   21 |     17 |       25 |      26s |       13s |        39s |     0.64 |
|   2 |   25 |     32 |       47 |    1m01s |       27s |      1m28s |     0.53 |
|   3 |   29 |     53 |       77 |    2m22s |       41s |      3m03s |     0.42 |
|   4 |   33 |     78 |      114 |    4m30s |       56s |      5m26s |     0.35 |
|   5 |   37 |    106 |      154 |    7m48s |     1m14s | !!!  9m02s |     0.28 |
|   6 |   41 |    134 |      195 |    6m54s |     1m36s |      8m30s |     0.38 |
|   7 |   45 |    154 |      224 |    8m48s |     2m31s |     11m19s |     0.33 |
|   8 |   49 |    192 |      279 |   13m00s |     3m14s |     16m14s |     0.29 |
|   9 |   53 |    230 |      335 |   19m09s |     3m37s | !!! 22m46s |     0.25 |
|  10 |   57 |    271 |      395 |   14m03s |     4m31s |     18m34s |     0.37 |
|  11 |   61 |    321 |      468 |   18m20s |     5m06s |     23m26s |     0.33 |



OPTIONS

1. Center

On by default. The QR code will be centered on the screen if enabled, otherwise it will be drawn in the top-left corner. (Originally, this behavior was fixed because it makes the math simpler and it's slightly faster in theory.)

2. StorePic 1

Off by default. If enabled, the program will save the QR code to Pic1 as soon as it finishes drawing. I wish there was a way to choose which Pic variable to store to, but there really isn't.

3. Alt Punct

Off by default. This is a weird feature that most people other than me probably won't care about, but here's the deal: because the calculator uses all upper-case letters by default, I figured Alphanumeric should be the premier encoding mode, as it lets you use the 10 digits, 26 upper-case letters, a space, and 8 punctuation characters. What more could you want? The problem is, these punctuation appear to have been chosen for encoding URIs and other technical stuff, and aren't ideal for composing a message. They are (enclosed in quotation marks) "$%*+-./:". Dollar sign and percent? Really? Could I please have a question mark or even a comma? So I created my own set of punctuation optimized for natural English: "?;',-.!:". Three of these are the same (hyphen, period, colon) and the rest are positioned so they line up with the symbol that looks the most similar. If you enable this mode, you can use this alternate set of punctuation, although if you scan the code on your phone, they'll get mapped back to the standard symbols. Depending on what you want to do with the data, you can write your own program on the other end that translates these characters back to the "useful" ones, but that's up to you.

4. ASCII Fix

Off by default. Another kind of weird feature. You may be aware that, since the calculator has no escape metacharacter for strings, it's impossible to put a quotation mark in a string. Or is it? You can actually do it if you manually type in a string when prompted by the Input command within a program, or transfer the string directly to your calculator. But since we can't put do it programatically, I use the pi symbol in its place when initializing the string in this program. However, if you want to fix the ASCII string yourself (remember, we're only using characters 32 to 127), then turn this option on so that Str3 doesn't get overwritten. You can even come up with an entirely new character set if you want. Note that if Str3 doesn't contain exactly 95 characters (perhaps because a different program did something with it or you screwed up), then you'll be back to the old ASCII-with-pi character set. Why does this need to be an option at all, you might ask? Isn't it safe enough to just do that length=95 check? Indeed, I believe it would be, but there's actually no way (AFAICT) to check if a string is defined in TI-Basic without erroring out in the negative case. Enabling this option really just tells the program to assume Str3 exists in some form or another.

5. Autonomous

E: Encoding
V: Version
Str1
list.BIN


VARIABLES USED

Str1: User input
Str2: Alphanumeric character set
Str3: ASCII character set (see "ASCII FIX")
L1-L6: Temporary data, mostly ECC bytes
listCW: Codewords. Contains the bytes used to draw the QR code.
listQR: Options