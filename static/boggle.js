"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");
const $wordScore = $(".wordScore");
const $gameScore = $(".gameScore");
const $clock = $(".time");

let gameId;
let timeRemaining;
let timerId;

const SCORE_WORD_ROUTE = '/api/score-word';
const GAME_LENGTH = 30000;

/** Start */

async function start() {
  let response = await axios.get("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
  timeRemaining = GAME_LENGTH;
  $clock.text(`Time Remaining: ${timeRemaining/1000} seconds`);
  timerId = setInterval(countDown, 1000);
}

/** Display board */

/**
 * Gets game board instance and populates the DOM with letters 
 */
function displayBoard(board) {
  $table.empty();
  // loop over board and create the DOM tr/td structure
  $table.append("<tbody>");
  const $tbody = $("tbody")

  for (let row of board) {
    let $trow = $("<tr>");

    for (let ltr of row) {
      let $ltr = $(`<td>${ltr}</td>`);
      $trow.append($ltr);
    }

    $tbody.append($trow);
  }

}

/**
 * Handles the submit form button click
 * Makes an axios POST request
 * 
*/
async function submitForm(evt) {
  evt.preventDefault();

  if (!timeRemaining) return;

  const word = $wordInput.val().toUpperCase();

  const resp = await axios({
    url: SCORE_WORD_ROUTE,
    method: 'POST',
    data: { gameId, word }
  })

  handleWordDisplay(resp.data, word);
  // clear form
  $wordInput.val("");
}

/**
 * Takes the API response data for word submission
 * If word not legal, displays message on screen 
 * If word is valid, adds it to word list in DOM
*/
function handleWordDisplay(data, word) {
  $message.empty();
  const { result, wordScore, gameScore } = data;
  $wordScore.text("Word Score: ");

  if (result === "ok") {
    $playedWords.append(`<li>${word}</li>`);
    showRunningScores(wordScore, gameScore);
  } else if (result === 'not-word') {
    $message.text(`${word} is not a valid word!`);
  } else if (result === 'not-on-board') {
    $message.text(`${word} is not on the board!`);
  } else {
    // duplicate
    $message.text(`${word} has already been submitted`);
  }
}

/** 
 * Takes the API response scores and shows them in the DOM
 * */  
function showRunningScores(wordScore, gameScore) {
  $wordScore.text(`Word Score: ${wordScore}`);
  $gameScore.text(`Game Score: ${gameScore}`);
}

function countDown() {
  timeRemaining -= 1000;
  $clock.text(`Time Remaining: ${timeRemaining/1000} seconds`);

  if (timeRemaining === 0) {
    clearInterval(timerId);
    $clock.text("GAME OVER!");
  }
}


$form.on("submit", submitForm)

start();
