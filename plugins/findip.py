from taiiwobot.plugin import Plugin

# import socket
try:
    from shodan import Shodan
except:
    Shodan = False


class FindIP(Plugin):
    def __init__(self, bot):
        self.bot = bot
        if not Shodan:
            print("Shodan not installed.")
            return
        self.api = Shodan("KpYC07EoGBtGarTFXCpjsspMVQ0a5Aus")  # don look
        self.interface = bot.util.Interface(
            "findip",  # command name
            # plugin description
            "Looks up an IP address with shodan. Args: <IP>",
            [  # Flags: "<short form> <long form> <description> <1=string or 0=bool>"
                # "o output Specifies the location of the output file 1",
            ],
            self.main,  # root function
            subcommands=[],
        ).listen()  # sets the on message callbacks and parses messages

    def main(self, message, *args):  # include your root flags here
        query = args[0]
        # socket.inet_aton(query)
        results = self.api.host(query)
        output = []
        output.append(
            "OS: "
            + str(results["os"])
            + "\tISP: "
            + str(results["data"][0]["isp"])
            + (
                "\tProduct: " + str(results["data"][0]["product"])
                if "product" in results["data"][0]
                else ""
            )
        )
        output.append(
            "City: "
            + str(results["city"])
            + "\tPostal code: "
            + str(results["postal_code"])
        )
        output.append(
            "Area code: "
            + str(results["area_code"])
            + "\t\tCountry code: "
            + str(results["country_code"])
        )
        output.append(
            "Region name: "
            + str(results["region_code"])
            + "\tCountry name: "
            + str(results["country_name"])
        )
        output.append(
            "Latitude: "
            + str(results["latitude"])
            + "\tLongitude: "
            + str(results["longitude"])
        )
        ports = []
        for data in results["data"]:
            port = data["port"]
            if not str(port) in ports:
                ports.append(str(port))
        output.append("Open ports: " + ", ".join(ports))
        self.bot.msg(message.target, self.bot.server.code_block("\n".join(output)))
