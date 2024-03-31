//
//  HistoryViewController.swift
//  GuessThreeLettersPersistentWithSettings
//
//  Created by Justin Rogers on 2/8/24.
//

import UIKit

class HistoryViewController: UIViewController {
    
    var model: ThreeLettersModel!
    
    @IBOutlet weak var historyTextView: UITextView!
    

    override func viewWillAppear(_ animated: Bool) {
        super.viewWillAppear(animated)
        updateHistory()
        
    }
    
    func updateHistory() {
        if let appDelegate = UIApplication.shared.delegate as? AppDelegate {
            model = appDelegate.theModel
        }
        var historyText = ""
        for game in model.gameHistory {
            historyText += "Attempts: \(game.attempts), Correct Letters: \(game.correctLetters), Last Guess: \(game.lastGuess)\n"
            }
            historyTextView.text = historyText
        }
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */


