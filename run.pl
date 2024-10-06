$| = 1;
my $resolution = 10;
for (my $hubs = 10; $hubs <= 50; $hubs += 5) {
	foreach my $val (0.01, 0.02, 0.03, 0.04, 0.05) {
		my $psum = 0;
		for (my $i = 0; $i < $resolution; $i++) {
			#print "$i $hubs $val\n";
			system("python3 fakepubs.py $hubs --samename $val > temp.out");
			my $out = `python3 porcidify.py temp.out`;
			my ($p) = $out =~ /global (\S+)/;
			$psum += $p;
		}
		print join("\t", $hubs, $val, $psum / $resolution), "\n";
	}
}
