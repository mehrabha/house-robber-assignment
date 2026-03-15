import pytest
from concurrent.futures import ThreadPoolExecutor, TimeoutError;
from houserobber_dfs import HouseRobberDFS
from houserobber_dp import HouseRobberDP

@pytest.fixture
def robber():
    return HouseRobberDFS()

def validate_heist(original_houses, time_limit, expected_score, actual_score, robbed_indices):
    """Detective function to verify the indexes returned make a valid, optimal robbery."""
    # 1. Did you get the math right?
    assert actual_score == expected_score, f"Expected {expected_score}, got {actual_score}"
    
    # 2. Did you rob the exact same house twice? (Looking for duplicates)
    assert len(robbed_indices) == len(set(robbed_indices)), "You robbed the same index twice! Cheater!"
    
    total_value = 0
    total_time = 0
    
    for idx in robbed_indices:
        # 3. Does this house even exist?
        assert 0 <= idx < len(original_houses), f"Index {idx} does not exist in the neighborhood!"
        
        total_value += original_houses[idx][0]
        total_time += original_houses[idx][1]
        
    # 4. Do the indexes actually sum up to your claimed score?
    assert total_value == actual_score, f"The houses at your indexes only total {total_value}, not {actual_score}"
    
    # 5. Did you outrun the cops?
    assert total_time <= time_limit, f"Your route took {total_time} hours. You're busted!"

# --- The Test Cases ---

def test_01_empty_neighborhood(robber):
    score, indices = robber.rob_houses([], 10)
    assert score == 0
    assert indices == []

def test_02_police_are_here(robber):
    original = [(100, 5), (50, 2)]
    score, indices = robber.rob_houses(original, 0)
    assert score == 0
    assert indices == []

def test_03_fortress_houses(robber):
    original = [(1000, 11), (5000, 20)]
    score, indices = robber.rob_houses(original, 10)
    assert score == 0
    assert indices == []

def test_04_rob_everything(robber):
    original = [(10, 2), (20, 3), (30, 4)]
    score, indices = robber.rob_houses(original, 10)
    validate_heist(original, 10, 60, score, indices)
    # If they robbed everything, the indices should be exactly 0, 1, and 2
    assert set(indices) == {0, 1, 2} 

def test_05_the_greedy_trap(robber):
    original = [(60, 5), (50, 3), (40, 2)]
    score, indices = robber.rob_houses(original, 5)
    validate_heist(original, 5, 90, score, indices)
    assert set(indices) == {1, 2} # The optimal houses are at index 1 and 2

def test_06_duplicate_houses(robber):
    original = [(50, 3), (50, 3), (50, 3)]
    score, indices = robber.rob_houses(original, 6)
    validate_heist(original, 6, 100, score, indices)

def test_07_empty_vaults(robber):
    original = [(0, 2), (100, 3)]
    score, indices = robber.rob_houses(original, 5)
    validate_heist(original, 5, 100, score, indices)

def test_08_unsorted_input(robber):
    original = [(10, 5), (100, 2), (50, 3)]
    score, indices = robber.rob_houses(original, 5)
    validate_heist(original, 5, 150, score, indices)
    assert set(indices) == {1, 2}

def test_09_large_dp_stress_test(robber):
    original = [(i, 1) for i in range(1, 1001)]
    time_limit = 500
    expected_score = sum(range(501, 1001))
    
    executor = ThreadPoolExecutor()
    future = executor.submit(robber.rob_houses, original, time_limit)

    try:
        score, indices = future.result(timeout=5)
        validate_heist(original, time_limit, expected_score, score, indices)
    except TimeoutError:
        pytest.fail("execution time limit exceeded!!")
    finally:
        executor.shutdown(wait=False)

def test_10_massive_capacity_test(robber):
    original = [(1000000, 50)] * 100
    time_limit = 5000
    expected_score = 100000000
    
    executor = ThreadPoolExecutor()
    try:
        future = executor.submit(robber.rob_houses, original, time_limit)
        score, indices = future.result(timeout=5)
        validate_heist(original, time_limit, expected_score, score, indices)
    except:
        pytest.fail("execution time limit exceed!!")
    finally:
        executor.shutdown(wait=False)

def test_11_the_memory_crusher(robber):
    """
    The N * W Trap.
    N = 5,000 houses. W = 10,000 hours.
    Your code will try to append 50,000,000 individual integers to lists.
    In native Python, the overhead of creating 5,000 massive lists and 
    constantly allocating memory for appending will likely exceed 10 seconds.
    """
    # 5000 identical houses taking 2 hours each
    original = [(10, 2)] * 5000 
    time_limit = 10000
    expected_score = 50000 # Can rob all of them

    executor = ThreadPoolExecutor()
    future = executor.submit(robber.rob_houses, original, time_limit)

    try:
        score, indices = future.result(timeout=10)
        assert score == expected_score
    except TimeoutError:
        pytest.fail("execution time limit exceeded!!")
    finally:
        executor.shutdown(wait=False)

def test_12_the_sparse_weight_trap(robber):
    """
    The Massive W Trap. 
    N = 10 houses. W = 100,000,000 hours.
    Your code will try to initialize a single list of 100 MILLION zeros. 
    It will instantly freeze, throttle your CPU, or throw a MemoryError.
    """
    # Just a few houses, but they take a massive amount of time
    original = [
        (500, 10000000), 
        (1000, 25000000), 
        (1500, 30000000),
        (2000, 45000000)
    ]
    time_limit = 100000000 
    
    executor = ThreadPoolExecutor()
    try:
        future = executor.submit(robber.rob_houses, original, time_limit)
        score, indices = future.result(timeout=10)
        assert score > 0
    except TimeoutError:
        pytest.fail("execution time limit exceeded")
    finally:
        executor.shutdown(wait=False)
