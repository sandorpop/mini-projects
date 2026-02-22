import json
    
class FileHandler:
    def __init__(self, filename):
        self.__filename = filename
        
    def read(self):
        try:
            with open(self.__filename) as file:
                content = file.read()
        except:
            raise ValueError("Error with file name")
        return json.loads(content)
    
class Player:
    def __init__(self, name, nationality, assists, goals, penalties, team, games):
        self.name = name
        self.nationality = nationality
        self.team = team
        self.assists = assists
        self.goals = goals
        self.penalties = penalties
        self.games = games
    
    def __str__(self):
        return f"{self.name:20} {self.team:3} {self.goals:>3} + {self.assists:>2} = {self.goals+self.assists:>3}"
    
    
class Stats:
    def __init__(self):
        self.__players = []
        
    def add_player(self, name, nationality, assists, goals, penalties, team, games):
        self.__players.append(Player(name, nationality, assists, goals, penalties, team, games))
    
    def search(self, name):
        return [player for player in self.__players if player.name == name]
    
    def all_entries(self):
        return self.__players
    
    
class StatsApplication:
    def __init__(self):
        self.__stats = Stats()
        
    def search(self):
        name = input("name: ")
        players = self.__stats.search(name)
        if len(players) == 0:
            print("no player found")
            return
        for player in players:
            print(player)
            
    def list_teams(self):
        teams = sorted(set([player.team for player in self.__stats.all_entries()]))
        for team in teams:
            print(team)
            
    def list_countries(self):
        countries = sorted(set([player.nationality for player in self.__stats.all_entries()]))
        for country in countries:
            print(country)
            
    def sort_by_points(self, players: list):
        
        def order_by_points(player: Player):
            return player.goals + player.assists, player.goals
        
        return sorted(players, key=order_by_points, reverse=True)
    
    def team_players(self):
        team = input("team: ")
        players = [player for player in self.__stats.all_entries() if player.team == team]
        for player in self.sort_by_points(players):
            print(player)
            
    def country_players(self):
        country = input("country: ")
        players = [player for player in self.__stats.all_entries() if player.nationality == country]
        for player in self.sort_by_points(players):
            print(player)
            
    def most_points(self):
        n = int(input("how many: "))
        for player in self.sort_by_points(self.__stats.all_entries())[:n]:
            print(player)
            
    def most_goals(self):
        n = int(input("how many: "))        
        players = sorted(self.__stats.all_entries(), key=lambda p:(-p.goals, p.games))
        for player in players[:n]:
            print(player)
            
    def help(self):
        print("commands:")
        print("0 quit")
        print("1 search for player")
        print("2 teams")
        print("3 countries")
        print("4 players in team")
        print("5 players from country")
        print("6 most points")
        print("7 most goals")
        
    def load_players(self):
        filename = input("file name: ")
        handler = FileHandler(filename)
        players = handler.read()
        for player in players:
            self.__stats.add_player(player["name"], player["nationality"], player["assists"], player["goals"], player["penalties"], player["team"], player["games"])
        print(f"read the data of {len(players)} players")
        print()
        
    def execute(self):
        self.load_players()
        self.help()
        
        while True:
            print()
            command = input("command: ")
            if command == "0":
                break
            elif command == "1":
                self.search()
            elif command == "2":
                self.list_teams()
            elif command == "3":
                self.list_countries()
            elif command == "4":
                self.team_players()
            elif command == "5":
                self.country_players()
            elif command == "6":
                self.most_points()
            elif command == "7":
                self.most_goals()
            else:
                self.help()
        
        
            
        
    
    
application = StatsApplication()
application.execute()
    
    
# handler = FileHandler("partial.json")
# partial = handler.read()

# print(partial)
# leon = Player("Leon Draisaitl","EDM", 43, 67)
# markus = Player("Markus Granlund", "EDM", 3, 1)
# mike = Player("Mike Green", "NJD", 3, 8)
# print(leon)
# print(mike)
# print(markus)
# print("123456789012345678901234567890123456789")