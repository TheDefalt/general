#! /usr/bin/ruby

require 'socket'
require 'timeout'

if ARGV.length < 3
	puts 'usage: ./scan.rb [TARGET] [START PORT] [STOP PORT]'
	exit
end

$rhost = ARGV[0]
$start = ARGV[1]
$stop = ARGV[2]

begin
	if (Integer $start) <= (Integer $stop)
		$to_scan = ((Integer $start)..(Integer $stop)).to_a
	else
		puts "invalid ports"
		exit
	end
rescue ArgumentError
	puts "invalid ports"
	exit
end

def scanport(port)
	s = Socket.new Socket::AF_INET, Socket::SOCK_STREAM
	begin
		sockaddr = Socket.pack_sockaddr_in(port, $rhost)
	rescue
		puts "failed to reach host"
		exit
	end
	timeout(10) do
		begin
			@result = s.connect(sockaddr)
		rescue
			return false
		end
	end
	if @result == 0
		return true
	else
		return false
	end
end

puts "beginning scan... \n\n"

$to_scan.each do |port|
	if scanport(port)
		puts "port " + port.to_s + ": open"
	end
end

puts "\nscan complete"
