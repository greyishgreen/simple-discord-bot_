import requests
from youtubesearchpython import Search
def coinlist():
  r=requests.get("https://api.coinlore.net/api/tickers/")
  veri= r.json()
  veri=veri.get('data')
  semboller=[]
  isimler=[]
  for i in veri:
    semboller.append(i.get('symbol').lower())
    isimler.append(i.get('name').lower())
  return semboller, isimler


def coin(mesaj):
  coinler=coinlist()
  semboller=coinler[0]
  isimler=coinler[1]
  mesaj=mesaj.lower()
  adet=1

  for s in semboller:
    if s in mesaj:
      sorgu=s
      sembolbul=True
      isimbul=False
      break
  for i in isimler:
    if i in mesaj:
      sorgu=i
      sembolbul=False
      isimbul=True
      break
  r=requests.get("https://api.coinlore.net/api/tickers/")
  veri= r.json()
  veri=veri.get('data')

  for kelime in mesaj.split(" "):
    if kelime.isnumeric():
      adet=float(kelime)
      break

  if sembolbul:
    for c in veri:
      if c.get('symbol').lower()==sorgu:
        return float(c.get('price_usd'))*adet
  if isimbul:
    for c in veri:
      if c.get('name').lower()==sorgu:
        return float(c.get('price_usd'))*adet
  return "bulunamadı"


def youtube(mesaj):
    sorgu= Search(mesaj, limit = 5)
    
    sorgu=sorgu.result()
    print(sorgu)
    videolar=[]
    for i in range(5):
        id=sorgu['result'][i]['id']

        video= f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{id}?si=p5ZwQjjfWG6MKbU3" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
        #video= f'<iframe width="560" height="315" src="https://www.youtube.com/embed/{id}si=MuUswpUxjwaD5Kxv" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>'
        videolar.append(video)
    return videolar


def hava_durumu(şehir):
  şehir=şehir.lower()
  r=requests.get(f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{şehir}?unitGroup=us&key=U7VS3ZLNPA52V85LLFMRX6KVF&contentType=json")
  veri= r.json()
  veri=veri.get('days')
  gün=veri[0].get('datetime')
  tempmin=veri[0].get('tempmin')
  tempmax=veri[0].get('tempmax')
  yağış=veri[0].get('preciptype')
  return(gün, tempmin, "-", tempmax, "derece", yağış)
    
  
  

#-------------------------------------------------
from discord.ext import commands 
import discord 

BOT_TOKEN="MTIwODQ1NjQ3OTA2MTgzOTkyNA.GLcSMj.hObiHIjbiMneoDcOZys2ATnDwDRLc0v1ENmH7o"
CHANNEL_ID=1208475219107250267

bot= commands.Bot(command_prefix="!", intents= discord.Intents.all())
komut_listesi = ["selam", "komutlar", "mesajcoin", "mesajyoutube", "hava"]

@bot.event
async def on_ready():
    print("Merhaba! Size nasıl yardımcı olabilirim?")
    channel=bot.get_channel(CHANNEL_ID)
    await channel.send("Merhaba! Size nasıl yardımcı olabilirim? Komut vermek için ! prefixini kullanabilirsiniz. Komutları öğrenmek için !komutlar yazabilirsiniz")

@bot.command()
async def selam(ctx):
    await ctx.send("merhaba!")

@bot.command()
async def komutlar(ctx):
    await ctx.send(komut_listesi)

@bot.command()
async def mesajcoin(ctx, mesaj1):
    await ctx.send(coin(mesaj1))
@bot.command()
async def mesajyoutube(ctx, mesaj1):    
    result = youtube(mesaj1)
    await ctx.send(result)

@bot.command()
async def hava(ctx, şehir):    
    await ctx.send(hava_durumu(şehir))



bot.run(BOT_TOKEN)

