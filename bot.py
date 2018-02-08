#Super simple bot example by Nicole Spin
#This code is based on example from Rapptz's discord wrapper
#https://github.com/Rapptz/discord.py
#License: MIT
import discord
import asyncio
import requests

client = discord.Client()

#Get market information using the Bittrex API
def get_market(pair):

    req_key = {'market': pair}
    base_url = 'https://bittrex.com/api/v1.1/public/getmarketsummary'
    market_txt = requests.get(base_url, req_key)
    r = market_txt.json()

    return r

#Arrange the reply message from the acquired JSON's style text.
def get_sentence(r):

    pair = r['result'][0]['MarketName']
    partition_ind = pair.find('-')
    base_currency = pair[:(partition_ind)]
    market_currency = pair[(partition_ind+1):]
    return "%s (Volume %lf %s)\nLast: %9.8lf %s (High: %9.8lf, Low: %9.8lf)\n" % \
            (r['result'][0]['MarketName'], r['result'][0]['BaseVolume'], base_currency, \
             r['result'][0]['Last'], base_currency, r['result'][0]['High'], r['result'][0]['Low'])

def get_sentence_usdt(r, usd_rate):

    #Get currency name
    pair = r['result'][0]['MarketName']
    partition_ind = pair.find('-')
    base_currency = pair[:(partition_ind)]
    market_currency = pair[(partition_ind+1):]
    #Calculate rate for USDT
    last_usd = r['result'][0]['Last'] * usd_rate
    high_usd = r['result'][0]['High'] * usd_rate
    low_usd = r['result'][0]['Low'] * usd_rate
    return "%s (Volume: %lf %s)\nLast: %9.8lf %s (High: %9.8lf, Low: %9.8lf)\nLast: %9.8lf USDT (High: %9.8lf, Low: %9.8lf)\n" % \
            (r['result'][0]['MarketName'], r['result'][0]['BaseVolume'], base_currency, r['result'][0]['Last'], base_currency, \
            r['result'][0]['High'], r['result'][0]['Low'],\
            last_usd, high_usd, low_usd)


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


@client.event
async def on_message(message):
    if message.content.startswith('!test'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1
        await client.edit_message(tmp, 'You have {} messages.'.format(counter))
    elif message.content.startswith('!sleep'):
        await asyncio.sleep(5)
        await client.send_message(message.channel, 'Done sleeping')

    elif message.content.startswith('!dgb_price'):
        counter = 0
        usd_btc = get_market('usdt-btc')
        btc_dgb = get_market('btc-dgb')
        MSG_btc = get_sentence_usdt(btc_dgb, usd_btc['result'][0]['Last'])
        tmp = await client.send_message(message.channel, MSG_btc)
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1

    elif message.content.startswith('!pdgb'):
        counter = 0
        usd_btc = get_market('usdt-btc')
        btc_dgb = get_market('btc-dgb')
        MSG_btc = get_sentence_usdt(btc_dgb, usd_btc['result'][0]['Last'])
        tmp = await client.send_message(message.channel, MSG_btc)
        async for log in client.logs_from(message.channel, limit=100):
            if log.author == message.author:
                counter += 1



client.run('YOUR TOKEN')
