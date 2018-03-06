{-# LANGUAGE OverloadedStrings   #-}
{-# LANGUAGE ScopedTypeVariables #-}

module Main where

import           Control.Monad
import           Data.Monoid
import           Data.Text          (Text)
import qualified Data.Text          as T
import           Data.Text.IO
import           Data.Time.Clock
import           Data.Time.Format
import qualified Grammar.Parse      as Parse
import           Grammar.Run
import           Grammar.Types
import           System.Environment
import           System.Random

main :: IO ()
main = do
  [amount, grammarFile] <- getArgs
  g <- Parse.grammarFromFile grammarFile
  titles <- genTitles g (read amount::Int)
  Data.Text.IO.putStr (T.unlines titles)

genTitles :: Grammar -> Int -> IO [Text]
genTitles grammar n = do
  mapM buildName [1..n]
    where buildName n = runTitle grammar "title"
  




  
