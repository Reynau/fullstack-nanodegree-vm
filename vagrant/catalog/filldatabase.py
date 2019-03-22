from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
from database_setup import Category, Base, Item
 
engine = create_engine('sqlite:///catalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

#Menu for UrbanBurger
category = Category(name = "Soccer")
session.add(category)
session.commit()

category2 = Category(name = "Basketball")
session.add(category2)
session.commit()

category3 = Category(name = "Baseball")
session.add(category3)
session.commit()

item = Item(name = "Veggie Burger", description = "Juicy grilled veggie patty with tomato mayo and lettuce", sub = "1", price = "$7.50", image="https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary-1500x1125.jpg", category = category)
session.add(item)
session.commit()

item = Item(name = "Veggie Burger 2", description = "Juicy grilled veggie patty with tomato mayo and lettuce", sub = "1", price = "$7.50", image="https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary-1500x1125.jpg", category = category)
session.add(item)
session.commit()

item = Item(name = "Veggie Burger 3", description = "Juicy grilled veggie patty with tomato mayo and lettuce", sub = "1", price = "$7.50", image="https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary-1500x1125.jpg", category = category2)
session.add(item)
session.commit()

item = Item(name = "Veggie Burger 4", description = "Juicy grilled veggie patty with tomato mayo and lettuce", sub = "1", price = "$7.50", image="https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary-1500x1125.jpg", category = category3)
session.add(item)
session.commit()

item = Item(name = "Veggie Burger 5", description = "Juicy grilled veggie patty with tomato mayo and lettuce", sub = "1", price = "$7.50", image="https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary-1500x1125.jpg", category = category2)
session.add(item)
session.commit()

item = Item(name = "Veggie Burger 6", description = "Juicy grilled veggie patty with tomato mayo and lettuce", sub = "1", price = "$7.50", image="https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary-1500x1125.jpg", category = category3)
session.add(item)
session.commit()

item = Item(name = "Veggie Burger 7", description = "Juicy grilled veggie patty with tomato mayo and lettuce", sub = "1", price = "$7.50", image="https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary-1500x1125.jpg", category = category3)
session.add(item)
session.commit()

item = Item(name = "Veggie Burger 8", description = "Juicy grilled veggie patty with tomato mayo and lettuce", sub = "1", price = "$7.50", image="https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary-1500x1125.jpg", category = category3)
session.add(item)
session.commit()

item = Item(name = "Veggie Burger 9", description = "Juicy grilled veggie patty with tomato mayo and lettuce", sub = "1", price = "$7.50", image="https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary-1500x1125.jpg", category = category)
session.add(item)
session.commit()

item = Item(name = "Veggie Burger 10", description = "Juicy grilled veggie patty with tomato mayo and lettuce", sub = "1", price = "$7.50", image="https://www.seriouseats.com/recipes/images/2015/07/20150702-sous-vide-hamburger-anova-primary-1500x1125.jpg", category = category)
session.add(item)
session.commit()