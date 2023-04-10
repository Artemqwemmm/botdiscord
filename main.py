import pycord
from pycord import commands

# создание клиента бота
client = commands.Bot(command_prefix='!')

# определение команды balance для вывода баланса пользователя
@client.command()
async def balance(ctx):
    user_id = str(ctx.author.id)
    balance = database.loc[database['user_id'] == user_id, 'balance']
    if len(balance) == 1:
        balance = balance.iloc[0]
        await ctx.send(f'{ctx.author.mention}, ваш баланс: {balance}')
    else:
        await ctx.send('Ошибка при получении баланса')

# определение команды transfer для перевода кредитов от одного пользователя другому
@client.command()
async def transfer(ctx, member: pycord.Member, amount: int):
    user_id = str(ctx.author.id)
    recipient_id = str(member.id)
    
    sender_balance = database.loc[database['user_id'] == user_id, 'balance'].item()
    recipient_balance = database.loc[database['user_id'] == recipient_id, 'balance'].item()
    
    if amount < sender_balance:
        database.loc[database['user_id'] == user_id, 'balance'] -= amount
        database.loc[database['user_id'] == recipient_id, 'balance'] += amount
        await ctx.send(f'{ctx.author.mention} перевел {amount} кредитов баланса на счет {member.mention}')
    else:
        await ctx.send(f'{ctx.author.mention}, у вас недостаточно средств на счету')

    database.to_csv('database.csv', index=False)

# запуск бота
client.run('')
