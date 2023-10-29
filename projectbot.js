// Import necessary libraries and dependencies
const discord = require('discord.js');
require('dotenv').config();
const axios = require('axios');

// Create a new Discord client and set up intents
const client = new discord.Client({intents:[discord.GatewayIntentBits.Guilds, discord.GatewayIntentBits.GuildMessages, discord.GatewayIntentBits.MessageContent]});

// Event listener for when the bot is ready
client.on('ready', () => {
  console.log(`Logged in as ${client.user.tag}!`);
});

// Event listener for when a message is received
client.on("messageCreate", on_message);

// Function to handle incoming messages
async function on_message(messageCreated) {
  // Ignore messages from bots to prevent infinite loops
  if (!messageCreated.author.bot) {
    // Define phrases that trigger the bot to suggest a song
    const phrases = ["suggest some music", "recommend me a song", "need new songs to listen to"];
    // Convert message content to lowercase for easier matching
    const lowerCaseContent = messageCreated.content.toLowerCase();
    // Check if message contains any of the trigger phrases
    if (phrases.some(phrase => lowerCaseContent.includes(phrase))) {
      console.log("A message has been received");
      try {
        // Send GET request to Spotify API to search for pop songs
        const response = await axios.get('https://api.spotify.com/v1/search', {
          params: {
            q: 'genre:"pop"',
            type: 'track',
            limit: 50
          },
          headers: {
            'Authorization': 'Bearer ' + process.env.SPOTIFY_API_TOKEN
          }
        });

        // Extract list of tracks from API response
        const tracks = response.data.tracks.items;
        // Choose a random track from the list
        const randomTrack = tracks[Math.floor(Math.random() * tracks.length)];

        // Create a message embed with song details and send it to the user
        const embed = new discord.MessageEmbed()
          .setColor('#1DB954')
          .setTitle(`Here's a song I recommend for you: ${randomTrack.name} by ${randomTrack.artists[0].name}`)
          .setURL(randomTrack.external_urls.spotify)
          .setThumbnail(randomTrack.album.images[0].url);

        messageCreated.reply({embeds: [embed]});
      } catch (error) {
        // Log error to console and send error message to user
        console.error(error);
        messageCreated.reply('Oops, something went wrong. Please try again later.');
      }
    }
  }
}

// Log in to the Discord client with your bot token
client.login('discord bot token');
