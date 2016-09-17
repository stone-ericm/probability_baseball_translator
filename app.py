class situation:
    
    #situations are defined from the perspective of the batting team. the inverse percentage is the winning percentage for the pitching team
    
    def __init__(self, **kwargs):
        self.inning = inning #1, 1.5, 2
        self.team = team #home = 1 /visitor = 0
        self.outs = outs #0, 1, 2
        self.base_sit = base_sit
        # 1 = nobody on
        # 2 = runner on 1st
        # 3 = runner on 2nd/
        # 4 = runners on 1st and 2nd/
        # 5 = runner on 3rd
        # 6 = runners on 1st and 3rd
        # 7 = runners on 2nd and 3rd/
        # 8 = bases loaded/
        self.net_score = net_score #batting team - pitching team
        self.occurences = 1
        self.won = 0 #did the batting team win?
        
