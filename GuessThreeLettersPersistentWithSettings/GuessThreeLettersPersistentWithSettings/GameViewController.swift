import UIKit

class GameViewController: UIViewController {
    
    // TODO: instantiate model object:
    var model: ThreeLettersModel!

    // TODO:  define an IBOutlet
    //    for each label that may need to be modified:
    @IBOutlet weak var guessLetter0Label: UILabel!
    @IBOutlet weak var guessLetter1Label: UILabel!
    @IBOutlet weak var guessLetter2Label: UILabel!
    
    @IBOutlet weak var resultLetter0Label: UILabel!
    @IBOutlet weak var resultLetter1Label: UILabel!
    @IBOutlet weak var resultLetter2Label: UILabel!
    
    @IBOutlet weak var attemptsLabel: UILabel!
    @IBOutlet weak var correctLettersLabel: UILabel!
    @IBOutlet weak var LastGuessLabel: UILabel!
    @IBOutlet weak var fastestGameLabel: UILabel!
    
    // TODO:  implement IBAction for Start New Game button:
    @IBAction func startGameButton(_ sender: Any) {
         print("in startGameButton()")
        // TODO: initialize text in three guess letter labels:
        guessLetter0Label.text = "a"
        guessLetter1Label.text = "a"
        guessLetter2Label.text = "a"

        // TODO: initialize text in three result letter labels:
        resultLetter0Label.text = "?"
        resultLetter1Label.text = "?"
        resultLetter2Label.text = "?"
        
        // TODO: set color for all three result letter labels:
        resultLetter0Label.backgroundColor = .white
        resultLetter1Label.backgroundColor = .white
        resultLetter2Label.backgroundColor = .white

        // TODO: ask model to start a new game:
        model.startGame()
        updateLabels()
        applyAlphabetRange()

    } // end of startGameButton

    // TODO: implement IBAction for Guess button:
    @IBAction func guessButton(_ sender: Any) {

        // TODO: obtain text from each one of the three guess letter labels,
        //       then concatenate into a string.
        guard let letter0 = guessLetter0Label.text,
              let letter1 = guessLetter1Label.text,
              let letter2 = guessLetter2Label.text else {
            return
        }

        // Note: labels are all optional types that may need unwrapping.

        // TODO: ask model to process the input:
        let guess = "\(letter0)\(letter1)\(letter2)"
        let correctLetters = model.processGuess(pGuess: guess)

        // TODO: update all information in corresponding labels,
        //       as from results in the model,
        //       e.g. number of attempts so far, etc.:
        updateLabels()
        if model.gameWon {
            applyWin()
        } else if model.gameOver {
            applyGameOver()
        }

        // TODO: check results for each letter in string,
        //       and update text for each correctly guessed letter label
        
        
        // TODO: check if current guess is fully correct,
        //    in which case change background color for all result letter labels,
        //    and update label showing fastest game so far so far:
        for i in 0..<correctLetters.count {
            if correctLetters[i]{
                switch i {
                case 0:
                    resultLetter0Label.text = String(guess[guess.index(guess.startIndex, offsetBy: i)])
                case 1:
                    resultLetter1Label.text = String(guess[guess.index(guess.startIndex, offsetBy: i)])
                case 2:
                    resultLetter2Label.text = String(guess[guess.index(guess.startIndex, offsetBy: i)])
                default:
                    break
                    
                }
            }
        }
        if correctLetters.allSatisfy({$0}) {
            endGame()
        }

    } // end of func guessButton()
    
    @IBAction func nextletter0Button() {
        incrementLetter(label: guessLetter0Label, position: 0)
    }
    
    @IBAction func nextLetter1Button() {
        incrementLetter(label: guessLetter1Label, position: 1)
    }
    
    @IBAction func nextLetter2Button() {
        incrementLetter(label: guessLetter2Label, position: 2)
    }
    
    @IBAction func prevLetter0Button() {
        decrementLetter(label: guessLetter0Label, position: 0)
    }

    @IBAction func prevLetter1Button() {
        decrementLetter(label: guessLetter1Label, position: 1)
    }

    @IBAction func prevLetter2Button() {
        decrementLetter(label: guessLetter2Label, position: 2)
    }

    func updateLabels() {
        attemptsLabel.text = "\(model.attempts)"
        correctLettersLabel.text = "\(model.correctLetters)"
        LastGuessLabel.text = "\(model.lastGuess)"
        fastestGameLabel.text = "Fastest Game: \(model.fastestGameSorFar)"
        
        if model.fastestGameSorFar == Int.max {
            fastestGameLabel.text = "Fastest Game: ∞ attempts"
        } else {
            fastestGameLabel.text = "Fastest Game: \(model.fastestGameSorFar) attempts"
        }
    }

    // TODO: implement IBAction for the other two "next letter" buttons:
    func incrementLetter(label: UILabel, position:Int) {
        let defaults = UserDefaults.standard
        let startLetter = defaults.string(forKey: "alphabetRangeStart") ?? "a"
        let endLetter = defaults.string(forKey: "alphabetRangeEnd") ?? "z"
            
        guard let currentLetter = label.text, let scalar = UnicodeScalar(currentLetter.lowercased()) else { return }
            
        var nextScalar: UnicodeScalar?
            
        if position == 0 {
            nextScalar = scalar.value < UnicodeScalar(endLetter.lowercased())?.value ?? scalar.value ? UnicodeScalar(scalar.value + 1): UnicodeScalar(startLetter.lowercased())
        } else {
            nextScalar = scalar.value < UnicodeScalar("z").value ? UnicodeScalar(scalar.value + 1): UnicodeScalar("a")
        }
            
        if let nextScalar = nextScalar {
            label.text = String(Character(nextScalar))
        }
    }

    // TODO: implement IBAction for each "previous letter" button:
    func decrementLetter(label: UILabel, position: Int) {
        let defaults = UserDefaults.standard
        let startLetter = defaults.string(forKey: "alphabetRangeStart") ?? "a"
        let endLetter = defaults.string(forKey: "alphabetRangeEnd") ?? "z"
        guard let currentLetter = label.text, let scalar = UnicodeScalar(currentLetter.lowercased()) else { return }
            
        var previousScalar: UnicodeScalar?
            
        if position == 0 {
            previousScalar = scalar.value > UnicodeScalar(startLetter.lowercased())?.value ?? scalar.value ? UnicodeScalar(scalar.value - 1): UnicodeScalar(endLetter.lowercased())
        }else {
            previousScalar = scalar.value > UnicodeScalar("a").value ? UnicodeScalar(scalar.value - 1): UnicodeScalar("z")
            }
            
        if let previousScalar = previousScalar {
            label.text = String(Character(previousScalar))
        }
    }
    
    func endGame() {
        model.stopGame(won: model.gameWon)
        updateLabels()
        
        if model.gameWon {
            applyWin()
        } else {
            applyGameOver()
        }
        
        model.save()
        
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        NotificationCenter.default.addObserver(self, selector: #selector(applyDarkMode), name: UIApplication.didBecomeActiveNotification, object: nil)
        applyDarkMode()
        self.title = "Guess Three Letters"
        if let appDelegate = UIApplication.shared.delegate as? AppDelegate {
            model = appDelegate.theModel
        }
        
        // Do any additional setup after loading the view.
    } // end of func viewDidLoad()
    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        applyAlphabetRange()
        applyDarkMode()
    }
    
    func applyAlphabetRange() {
        let defaults = UserDefaults.standard
        let startLetter = defaults.string(forKey: "alphabetRangeStart") ?? "a"
        guessLetter0Label.text = startLetter.lowercased()
        guessLetter1Label.text = "a"
        guessLetter2Label.text = "a"
    }
    
    @objc func applyDarkMode() {
        let defaults = UserDefaults.standard
        let darkModeEnabled = defaults.bool(forKey: "darkMode")
        overrideUserInterfaceStyle = darkModeEnabled ? .dark: .light
        view.backgroundColor = darkModeEnabled ? .black : .white
    }
    
    func applyGameOver() {
        self.resultLetter0Label.backgroundColor = .red
        self.resultLetter1Label.backgroundColor = .red
        self.resultLetter2Label.backgroundColor = .red
    }
    
    func applyWin() {
        self.resultLetter0Label.backgroundColor = .green
        self.resultLetter1Label.backgroundColor = .green
        self.resultLetter2Label.backgroundColor = .green
    }
} // end of class GameViewController: UIViewController
