import Foundation

struct Game {
    var attempts: Int
    var correctLetters: Int
    var lastGuess: String
}

class GameData: Codable {
    var attempts: [Int]
    init(attempts: [Int]) {
        self.attempts = attempts
    }
}
class ThreeLettersModel {
    var gameIsOn: Bool = false
    var gameOver: Bool = false
    var gameWon: Bool = false
    var fastestGameSorFar: Int = Int.max
    var gameData: GameData
    
    init(attempts: Int) {
        self.gameData = GameData(attempts: [attempts])
    }
    
    // provided 3-letter English words,
    //    starting with 'a' to 'm':
    let words = ["abs", "ace", "act", "add", "ads", "age", "ago", "aid", "all", "and",
                 "app", "arc", "ate", "awe", "ban", "bar", "bat", "bay", "bee", "bet",
                 "bid", "big", "bit", "boa", "bog", "boo", "bop", "bot", "bow", "box",
                 "boy", "bro", "bud", "bum", "bun", "bus", "but", "buy", "bye", "cab",
                 "can", "cap", "car", "cat", "dad", "did", "dig", "dip", "doe", "dot",
                 "dub", "dud", "dye", "ear", "eat", "eel", "egg", "ego", "emu", "end",
                 "err", "eve", "eye", "fat", "fax", "fee", "fit", "fix", "foe", "fog",
                 "fox", "fur", "gag", "gap", "gas", "gem", "gig", "gin", "git", "goo",
                 "gum", "gut", "ham", "hay", "hem", "hen", "her", "him", "his", "hot",
                 "how", "hue", "hug", "hum", "hut", "ion", "irk", "ivy", "jab", "jag",
                 "jam", "jar", "jaw", "jet", "jig", "jog", "kid", "kin", "kip", "kit",
                 "koi", "lab", "lad", "lax", "lay", "leg", "let", "lid", "lip", "lot",
                 "low", "lur", "map", "mar", "mat", "maw", "max", "may", "met", "mix",
                 "mob", "mom", "mop", "mud", "mug", "mum","nef","nil","nim","nop","now",
                 "oak","odd","off","oho","pad","pan","pay","peg","pel","qin","ram","red","rim","sac","sig","sit","ted","tee","til","uck","vac","van","vox","wad","wae","wan","xat","xis","yah","yap","zag","zig"]
    // TODO: add at least 20 more 3-letter English words,
    //    starting with 'n' to 'z',
    //    to make the game more complete.
    
    // TODO: state variables,
    //     e.g. to keep track of the number of attempts in the fastest game so far,
    //     the number of guesses in the current game,
    //     the current word to be guessed, etc.
    var gameHistory: [Game] = []
    var currentWord: String?
    var attempts: Int = 0
    var lastGuess: String = ""
    var correctLetters: Int = 0
    var maxAttempts = 0
    
    enum Difficulty: String {
        case easy = "easy"
        case medium = "medium"
        case hard = "hard"
        
        var maxGuesses: Int {
            switch self {
            case .easy:
                return 25
            case .medium:
                return 15
            case .hard:
                return 8
            }
        }
    }
    
    // TODO: implement startGame() method:
    func startGame() {
        let userDefaults = UserDefaults.standard
        let startLetter = userDefaults.string(forKey: "alphabetRangeStart")?.first ?? "a"
        let endLetter = userDefaults.string(forKey: "alphabetRangeEnd")?.first ?? "z"
        let selectedDifficulty = userDefaults.string(forKey: "difficultyLevel") ?? Difficulty.easy.rawValue
        let difficulty = Difficulty(rawValue: selectedDifficulty) ?? .easy
        maxAttempts = difficulty.maxGuesses
        gameOver = false
        gameWon = false
        
        print("Selected difficulty: \(difficulty.rawValue), Max attempts: \(maxAttempts)")
        
        let filteredWords = words.filter { word in
            guard let firstLetter = word.first else {
                return false
            }
            return startLetter...endLetter ~= firstLetter
        }
        
        if filteredWords.isEmpty {
            currentWord = "cat" // Example of a default word
            print("No words found for the selected range. Using a default word: \(currentWord!)")
        } else {
            let randomWordIndex = Int.random(in: 0..<filteredWords.count)
            currentWord = filteredWords[randomWordIndex]
        }
        
        attempts = 0
        lastGuess = ""
        correctLetters = 0
        gameIsOn = true
        print(currentWord!)
    }
    
    // TODO: implement stopGame() method:
    func stopGame(won: Bool = false) {
        gameIsOn = false
        gameWon = won
        gameOver = !won
        let gameRecord = Game(attempts: attempts, correctLetters: correctLetters, lastGuess: lastGuess)
        gameHistory.append(gameRecord)
        gameData.attempts.append(attempts)

    }
    
    // TODO: implement processGuess() method:
    func processGuess(pGuess: String ) -> [Bool] {
        guard gameIsOn else {
            print("Game is not currently active. Start a new game.")
            return []
        }

        lastGuess = pGuess
        attempts += 1
        if attempts > maxAttempts {
            print("Max attempts reached. Game over.")
            stopGame()
            return []
        }
        
        correctLetters = isTheGuessCorrect(pGuess: pGuess)
        let isGameWon = correctLetters == currentWord?.count
            
        updateFastestGame(isGameWon: isGameWon)
        if isGameWon {
            print("Congratulations! You've guessed correctly.")
            stopGame(won: true)
        }
        
        let game = Game(attempts: attempts, correctLetters: correctLetters, lastGuess: lastGuess)
        gameHistory.append(game)
        return getCorrectLettersArray(pGuess: pGuess)
       
    } // isTheGuess
    
    func isTheGuessCorrect(pGuess: String) -> Int {
        var correctLetters = 0
        for (index, char) in pGuess.enumerated() {
            let stringIndex = currentWord!.index(currentWord!.startIndex, offsetBy: index)
            if currentWord!.contains(char) && currentWord![stringIndex] == char {
                correctLetters += 1
            }
        }
        return correctLetters
    }
    
    func updateFastestGame(isGameWon: Bool) {
        if isGameWon && attempts < fastestGameSorFar {
            fastestGameSorFar = attempts
        }
    }
    
    func getCorrectLettersArray(pGuess: String) -> [Bool] {
        var correctLettersArray: [Bool] = [false, false, false]
        for (index, char) in pGuess.enumerated() {
            let stringIndex = currentWord!.index(currentWord!.startIndex, offsetBy: index)
            if currentWord![stringIndex] == char {
                correctLettersArray[index] = true
            }
        }
        return correctLettersArray
    }
    
    func save() {
        do {
            let data = try PropertyListEncoder().encode(gameData)
            let filePath = dataFilePath()
            try data.write(to: dataFilePath())
            print("Data saved to: \(filePath)")
        } catch {
            print("Error saving data: \(error)")
        }
    }
    
    func load() {
        let path = dataFilePath()
        if FileManager.default.fileExists(atPath: path.path){
            do {
                let data = try Data(contentsOf: path)
                let savedData = try PropertyListDecoder().decode(GameData.self, from: data)
                gameData = savedData
                attempts = savedData.attempts.last ?? 0
                print("Model loaded from \(path)")
            } catch {
                print("Error loading data: \(error)")
            }
        }
    }
    
    func dataFilePath() -> URL {
        let documentsDirectory = FileManager.default.urls(for: .documentDirectory, in: .userDomainMask).first!
        return documentsDirectory.appendingPathComponent("ThreeLettersModel.plist")
    }
    
} // end of class ThreeLettersModel
