"use strict";

const $playedWords = $("#words");
const $form = $("#newWordForm");
const $wordInput = $("#wordInput");
const $message = $(".msg");
const $table = $("table");

let gameId;
const SCORE_WORD_ROUTE = '/api/score-word';

/** Start */

async function start() {
  let response = await axios.get("/api/new-game");
  gameId = response.data.gameId;
  let board = response.data.board;

  displayBoard(board);
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

  const word = $wordInput.val().toUpperCase();

  const resp = await axios({
    url: SCORE_WORD_ROUTE,
    method: 'POST',
    data: { gameId, word }
  })

  const { result } = resp.data;
  handleWordDisplay(result, word)

}

/**
 * Takes the API response data for word submission
 * If word not legal, displays message on screen 
 * If word is valid, adds it to word list in DOM
*/
function handleWordDisplay(result, word) {
  $message.empty();

  if (result === "ok") {
    $playedWords.append(`<li>${word}</li>`);
  } else if (result === 'not-word') {
    $message.text(`${word} is not a valid word!`);
  } else {
    $message.text(`${word} is not on the board!`);
  }
}

$form.on("submit", submitForm)

start();