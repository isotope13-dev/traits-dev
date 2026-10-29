{ pkgs, ...}:

let
  homepage = pkgs.fetchgit {
    url = "https://code.hackerspace.pl/hswaw/printmaster.git";
    rev = "8a59d6d6421d4d169227e00379ede9723954f049";
    hash = "sha256-/svHDhfjdlxVKie7pVIz5AOlyQtgU1EOKTa4rx7KqKY=";
  };
in
{
  # Samba server exposed for the scanner - exposed on http://printmaster.waw.hackerspace.pl/brother/
  services.samba = {
    enable = true;
    openFirewall = true;

    settings = {
      global = {
        "security" = "user";

        "workgroup" = "WORKGROUP";
        "client min protocol" = "NT1";
        "server min protocol" = "NT1";
        "server string" = "printmaster";
        "netbios name" = "printmaster";
        
        # note: localhost is the ipv6 localhost ::1
        "hosts allow" = [ "10.8.1." "10.8.0." "127.0.0.1" "localhost" ];
        "hosts deny" = [ "0.0.0.0/0" ];
        "guest account" = "nobody";
        "map to guest" = "bad user";
      };

      brother = {
        "path" = "/run/brother";
        "browseable" = "yes";
        "read only" = "no";
        "guest ok" = "yes";
        "create mask" = "0644";
        "directory mask" = "0755";
        "force user" = "nobody";
        "force group" = "nogroup";
      };
    };
  };

  services.nginx = {
    enable = true;

    virtualHosts."label.waw.hackerspace.pl" = {
      locations."/".return = "302 https://label.hackerspace.pl$request_uri";
    };

    virtualHosts."printmaster.waw.hackerspace.pl" = {
      locations."/".root = homepage;

      locations."/brother/" = {
        alias = "/run/brother/";
        extraConfig = "autoindex on;";
      };

      locations."/printers/" = {
        proxyPass = "http://127.0.0.1:631";
        recommendedProxySettings = true;
      };
    };
  };

  systemd.tmpfiles.rules = [
      "d /run/brother 1777 nobody nogroup 1d"
  ];

  # FTP-to-mail proxy used for paperless
  systemd.services.ftpserver = let ftpserver-bin = pkgs.fetchzip {
      url = "https://github.com/fclairamb/ftpserver/releases/download/v0.13.0/ftpserver_0.13.0_linux_arm64.tar.gz";
      hash = "sha256-HMaE2vM4HpD80aUxt5mI0ZUexHT7XEOJPnHqwO+W01Q=";
      stripRoot = false;
    }; in {
    # TODO move ftpserver.json to secrets
    script = ''
      ${ftpserver-bin}/ftpserver -conf /etc/ftpserver.json
    '';

    after = [ "network.target" ];
    wantedBy = [ "multi-user.target" ];
  };

  networking.firewall.allowedTCPPorts = [
    # ftpserver
    2121

    # nginx
    80
  ];
}
